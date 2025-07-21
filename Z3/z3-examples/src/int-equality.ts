import { init } from 'z3-solver';
const { Context } = await init();
const Z3 = Context('main');

const x = Z3.Int.const('x');
const y = Z3.Int.const('y');

const conjecture = Z3.Eq(x, Z3.Sum(y, 2));
const solver = new Z3.Solver();
solver.add(conjecture);

const result = await solver.check();
if (result === "sat") {
    console.log(`Solution: ${solver.model()}`);
} else {
    console.log('No solution');
}
