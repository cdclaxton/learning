# Run plan detection experiments

import numpy as np

from reverse_cpt import *
from estimate_state_in_sequence import *


def perfect_stage_probability(changepoints, num_stages, tau_max):
    """Returns a matrix of stages given the changepoints."""

    assert num_stages > 0
    assert tau_max > 0

    m = np.zeros((num_stages, tau_max))

    current_stage = 0
    for i in range(tau_max):
        if i in changepoints:
            current_stage += 1
            assert current_stage < num_stages, f"Too many changepoints: {changepoints}"
        
        m[current_stage, i] = 1.0

    assert m.shape[0] == num_stages
    assert m.shape[1] == tau_max

    return m


def stages_squared_error(m1, m2):
    """Squared error of the stages."""

    assert m1.shape == m2.shape

    diff = m1 - m2
    return np.sum(diff**2)


def stages_error_using_most_likely(gt, m):
    """Error when using the most likely stage."""

    assert gt.shape == m.shape

    num_time_steps = gt.shape[1]
    err = np.zeros(num_time_steps)

    for i in range(num_time_steps):
        expected = np.argmax(gt[:,i])
        actual = np.argmax(m[:,i])
        if actual != expected:
            err[i] = 1.0

    return np.sum(err)


if __name__ == '__main__':

    # Generate a test data set
    num_stages = 3
    num_events = 5

    p_prop_lower = 0.1
    p_prop_upper = 0.9

    min_prob_p_e = 0.01
    max_prob_p_e = 0.3

    tau_max = 20

    s = generate_set(num_stages, num_events, p_prop_lower, p_prop_upper,
                     min_prob_p_e, max_prob_p_e)
    
    # Generate the ground truth stage and observed events
    gt_stages, event_times, event_types, gt_changepoints = generate_obs(s['p_s'], s['p_e_given_s'], tau_max)

    # Ground stage as a function of time index
    gt_stage_matrix = perfect_stage_probability(gt_changepoints, num_stages, tau_max)

    # Calculate the probability of the number of stages over time using known p(s) and p(e|s)
    m = prob_num_stages_over_time(event_times, event_types, s['p_s'], s['p_e_given_s'], tau_max)
    assert m.shape == (num_stages, tau_max)

    # Calculate the error between the ground truth and the stages
    err1a = stages_squared_error(gt_stage_matrix, m)
    err1b = stages_error_using_most_likely(gt_stage_matrix, m)
    print(f"Squared error: {err1a}, Most likely error: {err1b}")

    # Estimate p(e|s) from p(s|e) and p(s)
    p_e_hat = estimate_p_e(s['p_s_given_e'], s['p_s'], 0)
    p_s_hat = calc_p_s(s['p_s_given_e'], p_e_hat)
    p_e_given_s_hat = calc_p_e_given_s(s['p_s_given_e'], p_e_hat, p_s_hat)

    # Calculate the probability of the stage index over time using the estimate p(e|s)
    m2 = prob_num_stages_over_time(event_times, event_types, p_s_hat, p_e_given_s_hat, tau_max)
    assert m2.shape == (num_stages, tau_max)

    # Calculate the error between the ground truth and the stages using estimated p(e|s)
    err2a = stages_squared_error(gt_stage_matrix, m2)
    err2b = stages_error_using_most_likely(gt_stage_matrix, m2)
    print(f"Squared error: {err2a}, Most likely error: {err2b}")

    # Plot the stage indices over time
    fig = plt.figure()

    plt.subplot(2, 2, 1)
    plt.plot(event_times, event_types, 'x')
    plt.xlim(0, tau_max)
    for c in gt_changepoints:
        plt.axvline(x=c, color='r', ls=':')
    plt.xlabel('Time index')
    plt.ylabel('Event type')
    plt.title('Events')
    
    stage_colors = ['r', 'g', 'b']

    plt.subplot(2, 2, 2)
    for num_cps in range(m.shape[0]):
        plt.plot(gt_stage_matrix[num_cps, :], label=f"{num_cps + 1} stages", color=stage_colors[num_cps])
    for c in gt_changepoints:
        plt.axvline(x=c, color='r', ls=':')
    for e in event_times:
        plt.axvline(x=e, color='k', ls='--', alpha=0.2)     
    plt.xlabel('Time index')
    plt.ylabel('Probability of stage')
    plt.title('Ground truth')
    plt.legend()

    plt.subplot(2, 2, 3)
    for num_cps in range(m.shape[0]):
        plt.plot(m[num_cps, :], label=f"{num_cps + 1} stages", color=stage_colors[num_cps])
    for c in gt_changepoints:
        plt.axvline(x=c, color='r', ls=':')
    for e in event_times:
        plt.axvline(x=e, color='k', ls='--', alpha=0.2)        
    plt.xlabel('Time index')
    plt.ylabel('Probability of stage')
    plt.title('Known p(e|s)')
    plt.legend()

    plt.subplot(2, 2, 4)
    colors = ['r', 'g', 'b']
    for num_cps in range(m2.shape[0]):
        plt.plot(m2[num_cps, :], label=f"{num_cps + 1} stages", color=colors[num_cps])
    for c in gt_changepoints:
        plt.axvline(x=c, color='r', ls=':')
    for e in event_times:
        plt.axvline(x=e, color='k', ls='--', alpha=0.2)       
    plt.xlabel('Time index')
    plt.ylabel('Probability of stage')
    plt.title('Inferred p(e|s)')
    plt.legend()

    plt.tight_layout()
    plt.show()

    print(s['p_s'])
    print(p_s_hat)

    print(s['p_e_given_s'])
    print(p_e_given_s_hat)
    