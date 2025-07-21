import { init } from 'z3-solver';
const { Context } = await init();
const Z3 = Context('main');

const x = Z3.Bool.const('x');
const y = Z3.Bool.const('y');

const conjecture = Z3.Eq(
    Z3.Not(Z3.And(x, y)),
    Z3.Or(Z3.Not(x), Z3.Not(y))
)
const solver = new Z3.Solver();
solver.add(conjecture);
console.log(`De Morgan's law: ${await solver.check()}`);
