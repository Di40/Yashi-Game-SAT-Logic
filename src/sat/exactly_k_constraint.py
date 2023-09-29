from pysat.formula import WCNF
import itertools


def calculate_exactly_k_constraint(literals, k):
    phi_exactly_k = WCNF()
    num_literals = len(literals)

    if k < 0 or k > num_literals:
        raise ValueError("k must be between 0 and the number of literals")

    # At least k
    for combination in itertools.combinations(literals, num_literals - k + 1):
        clause = [lit for lit in combination]
        phi_exactly_k.append(clause)

    # Improvement: The following is not needed.
    # We deal with "At most k" lines using the "no cycles" constraint.
    # At most k
    # for combination in itertools.combinations(literals, k + 1):
    #     clause = [-lit for lit in combination]
    #     phi_exactly_k.append(clause)

    return phi_exactly_k
