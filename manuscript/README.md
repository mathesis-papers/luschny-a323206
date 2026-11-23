# OEIS A323206, COMMENTS (revision 52): Luschny's parity conjecture

For nonnegative integers `n,k`, the terminating polynomial `A(n,k)` has an
integer value, and it is odd if and only if `n` is even or `k+2` is a power
of two. The note proves this using ballot coefficients and Catalan parity.
It also proves a binary product for the polynomial, its number of odd
coefficients and degree modulo two, the extension to integer arguments,
formal generating and inverse identities, and parity formulas for
A323207, A323208, A323209, A323217, the linked rows and columns,
A064094 and the complete generalized ballot triangle A238762.

## Contents

- `note.tex`: complete mathematical statements, proofs and references.
- `metadata.json`: title, creators, CC BY 4.0 license and mathematical scope.
- `verify.py`: exact-arithmetic checks using only the Python standard library.
- `verification.json`: the expected deterministic output of the checker.

The companion PDF is `note.pdf`.

## Build and check

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a TeX installation with the packages named in `note.tex`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in the TeX file; a separate BibTeX pass is not
required. Run the finite checks with Python 3.10 or newer:

```sh
python3 verify.py > actual-verification.json
diff -u verification.json actual-verification.json
```

The result is `ALL_CHECKS_OK`: 5,151 coefficient identities and binary
supports, 102 additional boundary coefficients at `k=101`, 101 Catalan sums,
72 source examples, 4,141 integer evaluations and 404 diagonal or
antidiagonal identities. Further checks cover 102 binary products, support
counts and degrees, 5,151 values in each of the even-even and odd-odd ballot
slices, 10,201 mixed-parity zeros, 210 generating coefficients, 210 inverse
coefficients and 5,151 entries of A064094. Exact Catalan numbers are
generated independently by convolution and generalized ballot numbers by
their defining two-variable recurrence. These are finite checks; the
universal arguments are in the note.

## Sources and mathematical scope

The posing source is Peter Luschny's OEIS A323206, revision 52, NAME and
COMMENTS, March 15, 2026: <https://oeis.org/A323206>.
The conjecture first appears in revision 17, COMMENTS, February 21, 2019:
<https://oeis.org/history/view?seq=A323206&v=17>.
The ballot polynomials and their generating functions are classical;
Abate and Whitt (2011), equations (4), (9)--(10), use
`C_(k+1)(t)=P_k(t)`. Catalan parity is treated by Egecioglu (1983)
and the full binary valuation by Deutsch and Sagan (2004/2006), Theorem 2.1;
the note gives full references and self-contained proofs.

The declaration
`D5.S1.Recurrence.Invariants.LuschnyA323206Parity.result` has the full
nonnegative-index parity statement, including integrality:
<https://github.com/the-omega-institute/trureturing/blob/b0f7c01b01511ea00428c1b6edad5dd2b372eaf8/D5/S1/Recurrence/Invariants/LuschnyA323206Parity.lean>.
Its Catalan binary-support dependency is
`CatalanCompositionSquareParity.binary_catalan`:
<https://github.com/the-omega-institute/trureturing/blob/b0f7c01b01511ea00428c1b6edad5dd2b372eaf8/D5/S1/Recurrence/Invariants/CatalanCompositionSquareParity.lean>.
The negative-integer extension and coefficientwise and sequence
corollaries have the written proofs in the note.

## Creators and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`).
