"""Exact arithmetic for the A323206 polynomial and its parity consequences."""

import json
from fractions import Fraction
from math import comb, factorial, prod


SOURCE_ROWS = (
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 2, 5, 14, 42, 132, 429, 1430),
    (1, 3, 13, 67, 381, 2307, 14589, 95235),
    (1, 4, 25, 190, 1606, 14506, 137089, 1338790),
    (1, 5, 41, 413, 4641, 55797, 702297, 9137549),
    (1, 6, 61, 766, 10746, 161376, 2537781, 41260086),
    (1, 7, 85, 1279, 21517, 387607, 7312789, 142648495),
    (1, 8, 113, 1982, 38886, 817062, 17981769, 409186310),
    (1, 9, 145, 2905, 65121, 1563561, 39322929, 1022586105),
)
MAX_K = 100


def choose(upper, lower):
    return comb(upper, lower) if 0 <= lower <= upper else 0


def pochhammer(value, degree):
    return prod(value + offset for offset in range(degree))


def power_of_two(value):
    return value > 0 and value & (value - 1) == 0


def evaluate(coefficients, argument):
    value = 0
    for coefficient in reversed(coefficients):
        value = value * argument + coefficient
    return value


def multiply(left, right, limit):
    return [sum(left[index] * right[degree - index]
                for index in range(degree + 1)
                if index < len(left) and degree - index < len(right))
            for degree in range(limit + 1)]


def main():
    catalans = [1]
    for degree in range(MAX_K + 1):
        catalans.append(sum(catalans[index] * catalans[degree - index]
                            for index in range(degree + 1)))
    rows = []
    coefficient_count = 0
    for column in range(MAX_K + 2):
        coefficients = []
        for degree in range(column + 1):
            denominator = pochhammer(-column - 1, degree) * factorial(degree)
            assert denominator != 0
            rational = Fraction(pochhammer(-column, degree)
                                * pochhammer(column + 1, degree), denominator)
            ballot = choose(column + degree, degree) - choose(column + degree, degree - 1)
            assert rational.denominator == 1 and rational == ballot
            if degree:
                assert ballot == Fraction(column - degree + 1, degree) * choose(
                    column + degree, column + 1)
            assert (ballot % 2 == 1) == (degree & (column + 1) == 0)
            coefficients.append(ballot)
            if column <= MAX_K:
                coefficient_count += 1
        if column <= MAX_K:
            assert sum(coefficients) == catalans[column + 1]
            assert (catalans[column + 1] % 2 == 1) == power_of_two(column + 2)
        rows.append(tuple(coefficients))
    for column, coefficients in enumerate(rows):
        number = column + 1
        highest = number.bit_length() - 1
        support = {0}
        for digit in range(highest):
            if not (number >> digit) & 1:
                support |= {degree + 2 ** digit for degree in tuple(support)}
        actual = {degree for degree, coefficient in enumerate(coefficients)
                  if coefficient % 2}
        assert actual == support
        assert len(actual) == 2 ** (highest + 1 - number.bit_count())
        assert max(actual) == 2 ** (highest + 1) - number - 1
    ballot = {}
    for upper in range(2 * MAX_K + 2):
        for lower in range(upper + 1):
            if upper == lower == 0:
                ballot[lower, upper] = 1
            else:
                ballot[lower, upper] = (ballot.get((lower - 2, upper), 0)
                                       + ballot.get((lower, upper - 2), 0)
                                       + (upper % 2) * ballot.get((lower - 1, upper - 1), 0))
    mixed_count = 0
    for column in range(MAX_K + 1):
        for degree in range(column + 1):
            even = ballot[2 * degree, 2 * column]
            odd = ballot[2 * degree + 1, 2 * column + 1]
            assert even == rows[column][degree]
            assert odd == (column + degree + 1) * rows[column][degree]
            assert (odd % 2 == 1) == (degree & (column + 1) == 0
                                      and (column + degree) % 2 == 0)
            assert ballot[2 * degree, 2 * column + 1] == 0
            mixed_count += 1
        for degree in range(column):
            assert ballot[2 * degree + 1, 2 * column] == 0
            mixed_count += 1
    formal_limit = 20
    for argument in range(-3, 7):
        series = [1]
        for degree in range(1, formal_limit + 2):
            series.append(sum(catalans[index - 1] * argument ** (index - 1)
                              * series[degree - index]
                              for index in range(1, degree + 1)))
        for degree in range(formal_limit + 1):
            assert series[degree + 1] == evaluate(rows[degree], argument)
        inverse = [0] + series[1:formal_limit + 1]
        square = multiply(inverse, inverse, formal_limit)
        one_plus = [1] + inverse[1:]
        right_square = multiply(one_plus, one_plus, formal_limit)
        for degree in range(formal_limit + 1):
            assert inverse[degree] - (argument - 1) * square[degree] == (
                right_square[degree - 1] if degree else 0)
    triangle_count = 0
    for upper in range(MAX_K + 1):
        for argument in range(upper + 1):
            if upper == argument:
                value = 1
            else:
                length = upper - argument
                value = Fraction(sum((length - degree)
                                     * comb(length - 1 + degree, degree)
                                     * argument ** degree
                                     for degree in range(length)), length)
                assert value.denominator == 1
                assert value == evaluate(rows[length - 1], argument)
            assert (value % 2 == 1) == (upper == argument or argument % 2 == 0
                                        or power_of_two(upper - argument + 1))
            triangle_count += 1
    for argument, source_row in enumerate(SOURCE_ROWS):
        for column, expected in enumerate(source_row):
            assert evaluate(rows[column], argument) == expected
    for argument in range(-20, 21):
        for column in range(MAX_K + 1):
            value = evaluate(rows[column], argument)
            odd = argument % 2 == 0 or power_of_two(column + 2)
            assert (value % 2 == 1) == odd
            alternative = sum((choose(2 * column - degree, column)
                               - choose(2 * column - degree, column + 1))
                              * argument ** (column - degree)
                              for degree in range(column + 1))
            assert value == alternative
    for index in range(MAX_K + 1):
        assert (evaluate(rows[index], index) % 2 == 1) == (index % 2 == 0)
        assert (evaluate(rows[index + 1], index) % 2 == 1) == (
            index % 2 == 0 or power_of_two(index + 3))
        assert (evaluate(rows[index], index + 1) % 2 == 1) == (
            index % 2 == 1 or power_of_two(index + 2))
        antidiagonal = sum(evaluate(rows[column], index - column)
                           for column in range(index + 1))
        expected = index // 2 + 1
        if index % 2:
            expected += (index + 1).bit_length() - 1
        assert antidiagonal % 2 == expected % 2
    print(json.dumps({
        'status': 'ALL_CHECKS_OK',
        'arithmetic': 'exact integer and rational arithmetic',
        'coefficient_and_binary_support_cases': coefficient_count,
        'coefficient_range': '0 <= j <= k <= 100',
        'additional_boundary_coefficient_cases': len(rows[MAX_K + 1]),
        'catalan_row_sums': MAX_K + 1,
        'catalan_method': 'first-return convolution',
        'source_examples': 72,
        'source_example_range': '0 <= n <= 8, 0 <= k <= 7',
        'integer_evaluations': 41 * (MAX_K + 1),
        'integer_evaluation_range': '-20 <= t <= 20, 0 <= k <= 100',
        'diagonal_and_antidiagonal_cases': 4 * (MAX_K + 1),
        'diagonal_and_antidiagonal_range': '0 <= r <= 100',
        'binary_product_count_and_degree_cases': len(rows),
        'binary_product_range': '0 <= k <= 101',
        'generalized_ballot_even_even_cases': coefficient_count,
        'generalized_ballot_odd_odd_cases': coefficient_count,
        'generalized_ballot_mixed_parity_zeros': mixed_count,
        'generalized_ballot_method': 'two-variable defining recurrence',
        'formal_generating_coefficients': 10 * (formal_limit + 1),
        'formal_inverse_coefficients': 10 * (formal_limit + 1),
        'formal_series_range': '-3 <= t <= 6, degrees 0 through 20',
        'generalized_catalan_triangle_cases': triangle_count,
        'generalized_catalan_triangle_range': '0 <= m <= N <= 100',
        'scope': 'Finite identities and congruences; universal statements have written proofs in note.tex.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
