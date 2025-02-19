/* A wire */
wire(X, X).

/* NOT gate */
notGate(true, false).
notGate(false, true).

/* AND gate */
andGate(false, false, false).
andGate(false, true, false).
andGate(true, false, false).
andGate(true, true, true).

/* OR gate */
orGate(false, false, false).
orGate(false, true, true).
orGate(true, false, true).
orGate(true, true, true).

/* NAND gate */
nandGate(X, Y, Z) :- andGate(X, Y, W), notGate(W, Z).

/* NOR gate */
norGate(X, Y, Z) :- orGate(X, Y, W), notGate(W, Z).

/* XOR gate */
xorGate(false, false, false).
xorGate(false, true, true).
xorGate(true, false, true).
xorGate(true, true, false).