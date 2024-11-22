# Prioritisation system simulator
import random
import matplotlib.pyplot as plt
from scipy import stats


def bernoulli(p):
    """Function to generate a Bernoulli random variable."""
    assert 0.0 <= p <= 1.0

    def f():
        return random.random() <= p

    return f


def uniform_continuous(min_value, max_value):
    """Function to generate a number from a continuous uniform distribution."""
    assert min_value <= max_value
    scale = max_value - min_value

    def f():
        return stats.uniform.rvs(min_value, scale)

    return f


def uniform_discrete(min_value, max_value):
    """Function to generate a number from a discrete uniform distribution."""
    assert min_value <= max_value

    def f():
        return random.randint(min_value, max_value)

    return f


# Number of nominals for making the graphs (the higher the number, the closer
# the distribution to the true distribution)
n_nominals = 10000

n_days = 365
type_A = bernoulli(0.05)
analyst_working_on_day = bernoulli(0.8)

false_alert_generated = bernoulli(0.05)

# Type B nominal generators
prop_days_in_normal_state = uniform_continuous(0.7, 0.7)
true_alert_generated = bernoulli(0.95)
event_stopped_given_true_alert = bernoulli(0.95)
event_stopped_given_false_alert = bernoulli(0.9)


def num_false_positives_reviewed_in_normal(num_days):
    """Number of false positives reviewed in the normal state."""
    num_reviewed = 0
    for _ in range(num_days):
        if analyst_working_on_day() and false_alert_generated():
            num_reviewed += 1
    return num_reviewed


def type_A_false_positives_reviewed():
    """Number of false positives reviewed for a type A nominal."""
    return num_false_positives_reviewed_in_normal(n_days)


# Event outcomes
NO_EVENT = 0
EVENT_STOPPED_BY_TRUE_ALERT = 1
EVENT_STOPPED_BY_FALSE_ALERT = 2
EVENT_NOT_STOPPED = 4


def type_B():
    """Returns the number of false positives reviewed and whether the event was stopped."""

    # A type B has two states prior to the event
    n_days_in_normal_state = min(
        round(prop_days_in_normal_state() * n_days), n_days - 1
    )

    # Normal state
    n_false_positives_reviewed_normal = num_false_positives_reviewed_in_normal(
        n_days_in_normal_state
    )

    # Alert generated about precursor activity
    event_stopped = (
        analyst_working_on_day()
        and true_alert_generated()
        and event_stopped_given_true_alert()
    )
    if event_stopped:
        return (n_false_positives_reviewed_normal, EVENT_STOPPED_BY_TRUE_ALERT)

    # Precursor activity prior to event
    n_false_positives_reviewed_precursor = 0
    day = n_days_in_normal_state + 1
    while not event_stopped and day < n_days:
        if analyst_working_on_day() and false_alert_generated():
            event_stopped = event_stopped_given_false_alert()
            if not event_stopped:
                n_false_positives_reviewed_precursor += 1
        day += 1

    total_false_positives = (
        n_false_positives_reviewed_normal + n_false_positives_reviewed_precursor
    )

    if event_stopped:
        return (total_false_positives, EVENT_STOPPED_BY_FALSE_ALERT)

    return (total_false_positives, EVENT_NOT_STOPPED)


def simulate_nominal():
    """Simulate a single nominal."""

    nominal_is_type_A = type_A()

    if nominal_is_type_A:
        n_false_positives = type_A_false_positives_reviewed()
        return {
            "type": "A",
            "false_positives_reviewed": n_false_positives,
            "result": NO_EVENT,
        }

    n_false_positives, event_result = type_B()
    return {
        "type": "B",
        "false_positives_reviewed": n_false_positives,
        "result": event_result,
    }


def simulate_nominals(n_nominals):
    """Simulate n_nominals nominals."""

    false_positives = []
    event_outcomes = []

    for _ in range(n_nominals):
        s = simulate_nominal()
        false_positives.append(s["false_positives_reviewed"])
        event_outcomes.append(s["result"])

    return (false_positives, event_outcomes)


false_positives, event_outcomes = simulate_nominals(n_nominals)

fig, axs = plt.subplots(1, 2)
axs[0].hist(false_positives, density=True)
axs[0].set_xlabel("Number of false positives per nominal")
axs[0].set_ylabel("Probability")

n_stopped_by_true_alert = sum(
    [e == EVENT_STOPPED_BY_TRUE_ALERT for e in event_outcomes]
)
n_stopped_by_false_alert = sum(
    [e == EVENT_STOPPED_BY_FALSE_ALERT for e in event_outcomes]
)
n_event_not_stopped = sum([e == EVENT_NOT_STOPPED for e in event_outcomes])
events = ["Stopped by\ntrue alert", "Stopped by\nfalse alert", "Not stopped"]
counts = [n_stopped_by_true_alert, n_stopped_by_false_alert, n_event_not_stopped]
total = sum(counts)
for i in range(len(counts)):
    counts[i] = counts[i] / total

axs[1].bar(events, counts)
axs[1].set_xlabel("Event outcome")
axs[1].set_ylabel("Probability")
plt.show()
