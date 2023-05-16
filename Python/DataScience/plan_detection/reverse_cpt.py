# Reverse a CPT
#
# 

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as optimize

def probabilities_valid(x):
    """Is the vector of probabilities valid?"""

    return abs(sum(x) - 1.0) < 1e-6 and \
        all(x >= 0) and all(x <= 1)


def cpt_valid(m):
    """Is the CPT valid?"""

    for row_idx in range(m.shape[0]):
        if not probabilities_valid(m[row_idx,:]):
            return False
        
    return True


def generate_p_s(num_stages, p_prop_lower, p_prop_upper):
    """Randomly generate a p(s) for a given number of stages."""

    assert num_stages > 0
    assert 0 <= p_prop_lower <= p_prop_upper <= 1

    p = np.ones(num_stages)

    for i in range(1,num_stages):
        p[i] = p[i-1] * np.random.uniform(p_prop_lower, p_prop_upper)
    
    p = p / sum(p)

    assert probabilities_valid(p)

    return p



def generate_p_e_given_s(num_stages, num_events):
    """Randomly generate p(e|s)."""

    assert num_stages > 0
    assert num_events > 0

    alpha = np.ones(num_events)

    # Randomly generate each row (which must sum to 1)
    m = np.random.dirichlet(alpha, num_stages)

    assert m.shape[0] == num_stages
    assert m.shape[1] == num_events
    assert cpt_valid(m)

    return m


def calc_p_e(p_e_given_s, p_s):
    """Calculate p(e) from p(e|s) and p(s)."""

    assert p_e_given_s.shape[0] == len(p_s)

    p_e = np.dot(np.transpose(p_e_given_s), p_s)

    assert probabilities_valid(p_e)

    return p_e


def calc_p_s_given_e(p_e_given_s, p_s, p_e):
    """Calculate p(s|e) from p(e|s), p(s) and p(e) using Bayes' theorem."""

    assert p_e_given_s.shape[0] == len(p_s)
    assert p_e_given_s.shape[1] == len(p_e)

    num_events = len(p_e)
    num_stages = len(p_s)

    m = np.zeros((num_events, num_stages))

    for e in range(num_events):
        for s in range(num_stages):
            m[e,s] = p_e_given_s[s,e] * p_s[s] / p_e[e]

    assert m.shape[0] == num_events
    assert m.shape[1] == num_stages
    assert cpt_valid(m)

    return m
    

def p_e_within_bounds(p_e, min_prob, max_prob):
    """Is p(e) within the bounds of [min_prob, max_prob]?"""

    assert len(p_e) > 0
    assert 0 <= min_prob <= max_prob <= 1

    return all([min_prob <= p <= max_prob for p in p_e])


def calc_p_e_given_s(p_s_given_e, p_e, p_s):
    """Calculate p(e|s) from p(s|e), p(e) and p(s)."""
    
    assert len(p_e) > 0
    assert len(p_s) > 0
    assert p_s_given_e.shape[0] == len(p_e)
    assert p_s_given_e.shape[1] == len(p_s)

    num_events = len(p_e)
    num_stages = len(p_s)

    m = np.zeros((num_stages, num_events))

    for e in range(num_events):
        for s in range(num_stages):
            m[s,e] = p_s_given_e[e,s] * p_e[e] / p_s[s]
    
    assert m.shape[0] == num_stages
    assert m.shape[1] == num_events
    assert cpt_valid(m), f"CPT is invalid; row sums = {np.sum(m, axis=1)}, cpt = {m}"

    return m    


def cpt_error(m1, m2):
    """Find the squared error between the CPTs."""

    assert m1.shape == m2.shape
    
    return np.sum((m1 - m2)**2)


def generate_set(num_stages, num_events, p_prop_lower, p_prop_upper,
                 min_prob_p_e, max_prob_p_e):
    """Generate a set for an experiment."""

    assert num_stages > 0
    assert num_events > 0
    assert 0 <= p_prop_lower <= p_prop_upper <= 1
    assert 0 <= min_prob_p_e <= max_prob_p_e <= 1

    s = None

    while s is None:

        # Generate a random p(s)
        p_s = generate_p_s(num_stages, p_prop_lower, p_prop_upper)

        # Generate a random p(e|s)
        p_e_given_s = generate_p_e_given_s(num_stages, num_events)

        # Calculate p(e) from p(e|s) and p(s)
        p_e = calc_p_e(p_e_given_s, p_s)

        # Determine if p(e) is within the required bounds
        viable = p_e_within_bounds(p_e, min_prob_p_e, max_prob_p_e)
        if not viable:
            continue

        # Calculate p(s|e)
        p_s_given_e = calc_p_s_given_e(p_e_given_s, p_s, p_e)

        # Calculate p(e|s) as a validation check
        p_e_given_s_prime = calc_p_e_given_s(p_s_given_e, p_e, p_s)
        p_e_given_s_error = cpt_error(p_e_given_s, p_e_given_s_prime)
        assert p_e_given_s_error < 1e-5, f"error too large: {p_e_given_s_error}"

        s = {
            "p_s": p_s,
            "p_e_given_s": p_e_given_s,
            "p_e": p_e,
            "p_s_given_e": p_s_given_e
        }
    
    return s

def estimate_p_e(cpt_s_given_e, p_s, lam):
    """Estimate p(e) from p(s|e) and p(s)."""

    assert cpt_valid(cpt_s_given_e)
    assert probabilities_valid(p_s)
    assert lam >= 0

    cpt_s_given_e_t = cpt_s_given_e.transpose()

    # Number of different types of events
    N = cpt_s_given_e.shape[0]

    # Number of different stages
    M = cpt_s_given_e.shape[1]

    # Function to calculate the error given a candidate p(e)
    def f(e):
        p_e_err =  np.dot(cpt_s_given_e_t, e) - p_s
        reg_term = lam * np.dot(e, e)

        return np.dot(p_e_err, p_e_err) + reg_term

    # Constraints
    cons = ({
        'type': 'eq',
        'fun': lambda x: x.sum() - 1  # p(e) must sum to 1
    })

    # Bounds (each 0 <= p(e_i) <= 1)
    bnds = [(0, 1) for _ in range(N)]

    # Perform optimisation to find p(e)
    res = optimize.minimize(f, 
                            np.ones(N)/N,  # initial
                            method='SLSQP', 
                            constraints=cons, 
                            bounds=bnds,
                            tol=1e-30,
                            options={
                                'disp': False,
                                'maxiter': 10000,
                                'ftol': 1e-10,
                                'eps': 1e-10
                            })
    
    p_e_best = res['x']
    return p_e_best


def calc_p_s(cpt_s_given_e, p_e):
    """Calculate p(s) from p(s|e) and p(e)."""

    assert cpt_s_given_e.shape[0] == len(p_e)

    p_s = np.dot(np.transpose(cpt_s_given_e), p_e)

    assert len(p_s) == cpt_s_given_e.shape[1]

    return p_s


def calc_overall_error(p_e_given_s, p_e_given_s_hat, p_s, p_s_hat):
    """Calculate the error in p(e|s) and p(s)."""

    assert p_e_given_s.shape == p_e_given_s_hat.shape
    assert p_s.shape == p_s_hat.shape

    e1 = p_e_given_s - p_e_given_s_hat
    e1 = np.sum(e1**2)

    e2 = p_s - p_s_hat
    e2 = np.dot(e2, e2)

    return e1 + e2


def find_best_lambda(s, lambdas):
    """Find the value of lambda that minimises the error."""

    assert len(lambdas) > 0

    errs = [None for _ in range(len(lambdas))]

    for idx, l in enumerate(lambdas):

        # Estimate p(e) using optimisation
        p_e_hat = estimate_p_e(s['p_s_given_e'], s['p_s'], l)

        # Estimate p(s) given p(s|e) and estimated p_hat(e)
        p_s_hat = calc_p_s(s['p_s_given_e'], p_e_hat)    

        # Estimate p(e|s) given p_hat(e) and p_hat(s)
        p_e_given_s_hat = calc_p_e_given_s(s['p_s_given_e'], p_e_hat, p_s_hat)
        delta = p_e_given_s_hat - s['p_e_given_s']

        # Calculate the overall error in p(s) and p(e|s)
        errs[idx] = calc_overall_error(s['p_e_given_s'], p_e_given_s_hat, s['p_s'], p_s_hat)

    # Find the lowest error
    idx = np.argmin(errs)

    return lambdas[idx]


def run_experiments(num_stages, num_events,
                    p_prop_lower, p_prop_upper,
                    min_prob_p_e, max_prob_p_e,
                    num_experiments, 
                    lambdas):
    """Run a set of experiments to determine the best value of lambda."""

    assert num_experiments > 0
    assert len(lambdas) > 0

    best_lambdas = {}

    for i in range(num_experiments):
        
        print(f"Running experiment {i+1}/{num_experiments}")
        
        # Generate a dataset
        s = generate_set(num_stages, num_events, p_prop_lower, p_prop_upper,
                         min_prob_p_e, max_prob_p_e)
        
        best_lambda = find_best_lambda(s, lambdas)
        
        if best_lambda not in best_lambdas:
            best_lambdas[best_lambda] = 1
        else:
            best_lambdas[best_lambda] += 1
    
    return best_lambdas



if __name__ == '__main__':

    num_stages = 3
    num_events = 5

    p_prop_lower = 0.1
    p_prop_upper = 0.9

    min_prob_p_e = 0.01
    max_prob_p_e = 0.3

    s = generate_set(num_stages, num_events, p_prop_lower, p_prop_upper,
                     min_prob_p_e, max_prob_p_e)
    print(s)

    p_e_hat = estimate_p_e(s['p_s_given_e'], s['p_s'], 10)
    print(p_e_hat)

    # Estimate p(s) given p(s|e) and estimated p_hat(e)
    p_s_hat = calc_p_s(s['p_s_given_e'], p_e_hat)    

    # Estimate p(e|s) given p_hat(e) and p_hat(s)
    p_e_given_s_hat = calc_p_e_given_s(s['p_s_given_e'], p_e_hat, p_s_hat)
    delta = p_e_given_s_hat - s['p_e_given_s']
    print(delta)

    # Calculate the overall error in p(s) and p(e|s)
    err = calc_overall_error(s['p_e_given_s'], p_e_given_s_hat, s['p_s'], p_s_hat)
    print(err)

    min_lambda = 0
    max_lambda = 1
    delta_lambda = 0.01

    lambdas = np.arange(min_lambda, max_lambda + delta_lambda, delta_lambda)
    best_lambda = find_best_lambda(s, lambdas)
    print(best_lambda)

    # Run the experiments if required
    run_experiment = True
    if run_experiment:
        num_experiments = 100

        best_lambdas = run_experiments(num_stages, num_events,
                                       p_prop_lower, p_prop_upper,
                                       min_prob_p_e, max_prob_p_e,
                                       num_experiments, 
                                       lambdas)
        assert type(best_lambdas) == dict

        # Convert the sparse representation to non-sparse
        prop_exps_with_lambda = np.zeros(len(lambdas))
        for idx, l in enumerate(lambdas):
            if l in best_lambdas:
                prop_exps_with_lambda[idx] = best_lambdas[l]
        
        prop_exps_with_lambda = prop_exps_with_lambda / sum(prop_exps_with_lambda)

        # Create a plot
        plt.plot(lambdas, prop_exps_with_lambda, 'rx-')
        plt.xlim(min_lambda, max_lambda)
        plt.xlabel('$\lambda$')
        plt.ylabel('Proportion')
        plt.show()
