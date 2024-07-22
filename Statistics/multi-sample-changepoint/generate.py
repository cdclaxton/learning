import random
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta


num_minutes_in_day = 24 * 60


def continuous_uniform_gen(a, b):
    """Generator of samples from a continuous uniform distribution in the range [a,b]."""
    assert a < b

    def f():
        return stats.uniform.rvs(loc=a, scale=b - a)

    return f


def discrete_uniform_gen(a, b):
    """Generator of samples from a uniform distribution in the range [a,b]."""
    assert a <= b

    def f():
        return random.randint(a, b)

    return f


def normal_gen(mu, sigma):
    """Generator of samples from a normal distribution."""
    assert sigma > 0

    def f():
        return stats.norm.rvs(loc=mu, scale=sigma)

    return f


def inflated_poisson_gen(mu, min_value):
    """Generator of samples from an inflated Poisson distribution."""
    assert mu >= 0

    def f():
        v = stats.poisson.rvs(mu)
        if v < min_value:
            return min_value
        return v

    return f


def bernoulli(p):
    """Generator of Bernoulli samples."""
    assert 0.0 <= p <= 1.0

    def f():
        if random.random() < p:
            return 1
        else:
            return 0

    return f


def lead_scores(
    p_event_gen,
    p_changepoint_effect,
    start_day,
    initial_score,
    data_window,
    delta_before,
    delta_after,
):
    """Generates scores for a single lead."""

    # Probability that an event occurs on a given day
    event_occurs = bernoulli(p_event_gen())

    # Is the lead affected by a changepoint?
    is_affected_by_changepoint = bernoulli(p_changepoint_effect)() == 1

    # Initial sample
    samples = [(start_day(), initial_score())]

    # Generate subsequent samples
    for day in range(samples[0][0] + 1, data_window):
        if event_occurs() == 0:
            continue

        if not is_affected_by_changepoint or (
            is_affected_by_changepoint and day < changepoint_day
        ):
            new_score = samples[-1][1] + delta_before()
        else:
            new_score = samples[-1][1] + delta_after()

        samples.append((day, new_score))

    return samples


def day_to_timestamp(day, current_time, data_window):
    """Convert an integer day to a timestamp."""

    # Today at midnight (start of the day)
    today = datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        tzinfo=current_time.tzinfo,
    )

    num_days_ago = data_window - day - 1
    event_day = today - timedelta(days=num_days_ago)

    mu = num_minutes_in_day / 2
    sigma = 180
    minutes = stats.norm.rvs(loc=mu, scale=sigma)
    if minutes < 0:
        minutes = 0
    elif minutes >= num_minutes_in_day:
        minutes = num_minutes_in_day - 1

    return event_day + timedelta(minutes=minutes)


def set_times(samples, current_time, data_window):
    """Change a sample's day to a timestamp."""

    return [(day_to_timestamp(s[0], current_time, data_window), s[1]) for s in samples]


if __name__ == "__main__":

    number_of_leads = 100

    # Width of the data window in days
    data_window = 2 * 365

    # Distribution of the start day of a lead
    start_day = discrete_uniform_gen(0, 182)

    # Distribution of the initial score of a lead
    initial_score = normal_gen(50, 20)

    # Distribution of the probability of an event occurring on a given day
    p_event_gen = continuous_uniform_gen(1 / 365, 30 / 365)

    # Day of the changepoint
    changepoint_day = discrete_uniform_gen(
        int(data_window * 0.5), int(data_window * 0.6)
    )()

    # Probability that a lead is affected by the changepoint
    p_changepoint_effect = 0.7

    # Distribution of the change in a lead's score before the changepoint
    delta_before = normal_gen(5, 2)

    # Distribution of the change in a lead's score after the changepoint
    delta_after = normal_gen(-3, 2)

    leads = []
    for _ in range(number_of_leads):

        # Generate the scores for a lead
        samples = lead_scores(
            p_event_gen,
            p_changepoint_effect,
            start_day,
            initial_score,
            data_window,
            delta_before,
            delta_after,
        )

        leads.append(set_times(samples, datetime.now(), data_window))

    # Plot the samples for the leads
    for lead in leads:
        days = [s[0] for s in lead]
        scores = [s[1] for s in lead]
        plt.plot(days, scores, color="b", alpha=0.3)

    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.show()
