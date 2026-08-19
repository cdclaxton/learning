from itertools import product

import pyagrum as gum
import pyagrum.lib.image as gimg


def calc_posterior_using_pyagrum(p_a, b_cpts, p_b):

    # Number of instances of node b
    N = len(b_cpts)

    # Instantiate the Bayesian network
    bn = gum.BayesNet("Bayes Net")

    # Node a (with 2 states)
    a = bn.add(gum.LabelizedVariable("a", "a", 2))

    # Set node a's CPT
    bn.cpt("a")[:] = p_a

    b_nodes = []
    for i in range(N):
        # Create the b_i node
        b_node_name = f"b_{i}"
        b_node = bn.add(gum.LabelizedVariable(b_node_name, b_node_name, 2))
        b_nodes.append(b_node)

        # Add an arc from a to b_i
        bn.addArc(a, b_nodes[-1])

        # Define the CPT p(b_i|a)
        bn.cpt(b_node_name)[:] = b_cpts[i]

    # Define the evidence
    evidence = {f"b_{i}": [1 - p_b[i], p_b[i]] for i in range(N)}

    # Export the network as a PNG
    gimg.exportInference(bn, "network-soft-evidence.png", evs=evidence)

    # Perform exact inference
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()
    return ie.posterior("a")[1]


def build_soft_evidence_cpt(p):
    return [
        [p, 1 - p],
        [1 - p, p],
    ]


def check_result(p_a, b_cpts, p_b):

    # Number of instances of node b
    N = len(b_cpts)

    # Instantiate the Bayesian network
    bn = gum.BayesNet("Bayes Net")

    # Node a (with 2 states)
    a = bn.add(gum.LabelizedVariable("a", "a", 2))

    # Set node a's CPT
    bn.cpt("a")[:] = p_a

    b_nodes = []
    c_nodes = []
    for i in range(N):
        # Create the b_i node
        b_node_name = f"b_{i}"
        b_node = bn.add(gum.LabelizedVariable(b_node_name, b_node_name, 2))
        b_nodes.append(b_node)

        # Add an arc from a to b_i
        bn.addArc(a, b_nodes[-1])

        # Define the CPT p(b_i|a)
        bn.cpt(b_node_name)[:] = b_cpts[i]

        # Create the c_i node
        c_node_name = f"c_{i}"
        c_node = bn.add(gum.LabelizedVariable(c_node_name, c_node_name, 2))
        c_nodes.append(c_node)

        # Add an arc from b_i to c_i
        bn.addArc(b_nodes[-1], c_nodes[-1])

        # Define the CPT p(c_i|b_i)
        bn.cpt(c_node_name)[:] = build_soft_evidence_cpt(p_b[i])

    # Define the evidence
    evidence = {f"c_{i}": 1 for i in range(N)}

    # Export the network as a PNG
    gimg.exportInference(bn, "network.png", evs=evidence)

    # Perform exact inference
    ie = gum.LazyPropagation(bn)
    ie.setEvidence(evidence)
    ie.makeInference()
    return ie.posterior("a")[1]


def generate_binary(n: int) -> list[list[bool]]:
    return [list(p) for p in product([0, 1], repeat=n)]


def calc_joint_marginal(p_a, b_cpts, p_b, a):
    assert a == 0 or a == 1

    N = len(b_cpts)

    # Build the CPTs p(c_i|b_i)
    c_cpts = [build_soft_evidence_cpt(p_b[i]) for i in range(N)]

    total = 0

    for b in generate_binary(N):
        product_term = 1
        for i in range(N):
            # Note the indexing is reversed due to how the CPTs are formed
            product_term *= b_cpts[i][a][b[i]] * c_cpts[i][b[i]][1]

        total += product_term

    return p_a[a] * total


def calc_marginal_conditional(p_a, b_cpts, p_b):
    """Calculate p(a=1|c=1)"""

    p0 = calc_joint_marginal(p_a, b_cpts, p_b, 0)
    p1 = calc_joint_marginal(p_a, b_cpts, p_b, 1)

    return p1 / (p0 + p1)


if __name__ == "__main__":
    # Prior probability [p(a = 0), p(a = 1)]
    p_a = [0.4, 0.6]

    # Define the CPTs p(b_i|a) for each b_i
    b_cpts = [
        [
            [0.6, 0.4],
            [0.3, 0.7],
        ],
        [
            [0.9, 0.1],
            [0.2, 0.8],
        ],
    ]

    # Soft evidence for each b_i
    p_b = [0.9, 0.7]

    # Calculate the marginal posterior probability p(a|b)
    posterior_p_a = calc_marginal_conditional(p_a, b_cpts, p_b)
    print(f"Posterior: {posterior_p_a}")

    # Check the result using PyAgrum
    posterior_p_a_pyagrum = check_result(p_a, b_cpts, p_b)
    print(f"Posterior (using PyAgrum): {posterior_p_a_pyagrum}")

    # Calculate the posterior condition with soft evidence using PyAgrum
    result = calc_posterior_using_pyagrum(p_a, b_cpts, p_b)
    print(f"Posterior conditional with soft evidence using PyAgrum: {result}")
