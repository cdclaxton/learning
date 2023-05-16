import numpy as np
import pytest

from estimate_state_in_sequence import *

def test_stage_changepoints():
    """Unit tests for stage_changepoints()."""

    number_tests_per_num_stages = 100
    
    for num_stages in range(2, 6):
        for _ in range(number_tests_per_num_stages):
            tau_max = np.random.randint(6, 100)
            changepoints = stage_changepoints(num_stages, tau_max)

            assert len(changepoints) == num_stages - 1
            assert len(set(changepoints)) == len(changepoints)
            assert max(changepoints) < tau_max


def test_gen_events_for_stage():
    """Unit tests for gen_events_for_stage()."""

    # gen_events_for_stage() has lots of pre and post conditions, so this
    # test just exercies the function with different parameters
    t_min = np.random.randint(0, 10000)
    delta = np.random.randint(0, 100)
    t_max = t_min + delta

    event_times, event_types = gen_events_for_stage(t_min, t_max, [0.2, 0.8])
    assert len(event_times) == len(event_types)


def test_cpt_is_valid():
    """Unit tests for check_cpt_is_valid()."""

    assert check_cpt_is_valid(np.array([
        [0.5, 0.5],
        [0.2, 0.8],
        [1.0, 0.0],
        [0.0, 1.0]
    ]))

    assert not check_cpt_is_valid(np.array([
        [0.5, 0.6],
        [0.2, 0.8],
        [1.0, 0.0],
        [0.0, 1.0]
    ]))    


def test_check_probs_sum_to_1():
    """Unit tests for check_probs_sum_to_1()."""

    assert check_probs_sum_to_1([0.2, 0.8])
    assert not check_probs_sum_to_1([0.2, 0.9])


def test_generate_obs():
    """Unit tests for generate_obs()."""

    # CPT p(e|s)
    cpt = np.array([
        [0.2, 0.8],
        [1.0, 0.0],
        [0.0, 1.0]
    ])

    tau_max = 20

    # Only one stage
    p_s = np.array([1.0, 0.0, 0.0])
    gt_stages, event_times, event_types, changepoints = generate_obs(p_s, cpt, tau_max)
    assert len(changepoints) == 0
    assert set(gt_stages) == {0}    

    # Two stages
    p_s = np.array([0.0, 1.0, 0.0])
    gt_stages, event_times, event_types, changepoints = generate_obs(p_s, cpt, tau_max)
    assert len(changepoints) == 1
    assert set(gt_stages) == {0, 1}    

    # Three stages
    p_s = np.array([0.0, 0.0, 1.0])
    gt_stages, event_times, event_types, changepoints = generate_obs(p_s, cpt, tau_max)
    assert len(changepoints) == 2
    assert set(gt_stages) == {0, 1, 2}    


def test_indicator():
    """Unit tests for indicator()."""

    # One stage (no changepoints)
    assert indicator(0, 0, [], 20) == 1.0
    assert indicator(19, 0, [], 20) == 1.0

    # Two stages (1 changepoint)
    assert indicator(0, 0, [10], 20) == 1.0
    assert indicator(9, 0, [10], 20) == 1.0
    assert indicator(10, 0, [10], 20) == 0.0
    assert indicator(0, 1, [10], 20) == 0.0
    assert indicator(9, 1, [10], 20) == 0.0
    assert indicator(10, 1, [10], 20) == 1.0
    assert indicator(19, 1, [10], 20) == 1.0

    # Three stages (2 changepoints)
    assert indicator(0, 0, [10, 15], 20) == 1.0
    assert indicator(0, 1, [10, 15], 20) == 0.0
    assert indicator(0, 2, [10, 15], 20) == 0.0
    assert indicator(10, 0, [10, 15], 20) == 0.0
    assert indicator(10, 1, [10, 15], 20) == 1.0
    assert indicator(10, 2, [10, 15], 20) == 0.0
    assert indicator(15, 0, [10, 15], 20) == 0.0
    assert indicator(15, 1, [10, 15], 20) == 0.0
    assert indicator(15, 2, [10, 15], 20) == 1.0
    assert indicator(19, 2, [10, 15], 20) == 1.0

def test_log_likelihood():

    cpt = np.array([
        [0.2, 0.5, 0.3],
        [0.7, 0.1, 0.2],
        [0.3, 0.2, 0.5]
    ])

    # event_times, event_types, changepoints, tau_max, expected log likelihood
    test_cases = [
        [ [0], [0], [5, 9], 10, math.log(0.2) ], # stage 0
        [ [6], [0], [5, 9], 10, math.log(0.7) ], # stage 1
        [ [9], [0], [5, 9], 10, math.log(0.3) ], # stage 2
        [ [0, 4], [0, 0], [5, 9], 10, math.log(0.2) + math.log(0.2) ], # 2 x stage 0
        [ [0, 4], [0, 1], [5, 9], 10, math.log(0.2) + math.log(0.5) ], # 2 x stage 0
        [ [5, 4], [0, 1], [5, 9], 10, math.log(0.7) + math.log(0.5) ], # stage 1, 0
        [ [4, 5, 9], [0, 1, 2], [5, 9], 10, math.log(0.2) + math.log(0.1) + math.log(0.5) ], # stage 0, 1, 2
    ]
    
    for t in test_cases:
        event_times, event_types, changepoints, tau_max, expected = t
        actual = log_likelihood(event_times, event_types, changepoints, cpt, tau_max)
        assert abs(actual - expected) < 1e-6, f"actual: {actual}, expected: {expected}"


def test_valid_changepoints():
    """Unit tests for valid_changepoints()."""

    assert valid_changepoints([0])
    assert not valid_changepoints([0, 0])
    assert valid_changepoints([0, 1])
    assert valid_changepoints([0, 2])
    assert not valid_changepoints([1, 0])
    assert not valid_changepoints([1, 1])
    assert valid_changepoints([0, 1, 2])
    assert not valid_changepoints([0, 1, 1])
    assert not valid_changepoints([0, 2, 1])
    assert not valid_changepoints([2, 0, 1])


def test_all_changepoints():
    """Unit tests for all_changepoints()."""

    assert all_changepoints(0, 3) == []
    assert all_changepoints(1, 3) == [(0, ), (1, ), (2, )]    
    assert all_changepoints(2, 3) == [(0, 1), (0, 2), (1, 2)]
    assert all_changepoints(2, 4) == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert all_changepoints(3, 4) == [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def test_trim_events():
    """Unit tests for trim_events()."""

    test_cases = [
        {
            "event_times": np.array([0, 3]),
            "event_types": np.array([1, 2]),
            "t": 0,
            "exp_times": np.array([0]),
            "exp_types": np.array([1])
        },
        {
            "event_times": np.array([0, 3]),
            "event_types": np.array([1, 2]),
            "t": 1,
            "exp_times": np.array([0]),
            "exp_types": np.array([1])
        },
                {
            "event_times": np.array([0, 3]),
            "event_types": np.array([1, 2]),
            "t": 3,
            "exp_times": np.array([0, 3]),
            "exp_types": np.array([1, 2])
        },
    ]

    for t in test_cases:
        actual_times, actual_types = trim_events(t["event_times"], 
                                                 t["event_types"], 
                                                 t["t"])
        assert np.allclose(actual_times, t["exp_times"])
        assert np.allclose(actual_types, t["exp_types"])


def test_calc_cpt_event_given_stage():
    """Unit tests for calc_cpt_event_given_stage()."""

    # CPT of p(s|e) with 3 events and 2 stages
    p_s_given_e = np.array([
        [0.1, 0.9],
        [0.8, 0.2],
        [0.6, 0.4]
    ])

    # p(s)
    p_s = np.array([0.64, 0.36])

    # p(e|s), p(e)
    p_e_given_s, p_e = calc_cpt_event_given_stage(p_s_given_e, p_s)

    p_e_expected = np.array([0.2, 0.7, 0.1])

    # Check the expected values
    p_s_hat = np.dot( np.transpose(p_s_given_e), p_e_expected )
    delta = p_s_hat - p_s
    err = np.dot(delta, delta)
    assert err < 1e-6, f"p_s_hat outside bounds, squared error = {err}, delta = {delta}"

    delta = p_e_expected - p_e
    err = np.dot(delta, delta)
    assert err < 1e-3, f"p_e outside bounds, squared error = {err}, delta = {delta}"

    p_e_given_s_expected = np.array([
        [0.1*0.2/0.64, 0.8*0.7/0.64, 0.6*0.1/0.64],
        [0.9*0.2/0.36, 0.2*0.7/0.36, 0.4*0.1/0.36]
    ])

    delta = p_e_given_s_expected - p_e_given_s
    err = np.sum(delta**2)
    assert err < 1e-6, f"squared error: {err}, delta: {delta}"