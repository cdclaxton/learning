import { init } from 'z3-solver';
const { Context } = await init();
const Z3 = Context('main');

const x = Z3.Int.const('x');

const solver = new Z3.Solver();
solver.add(Z3.And(x.ge(0), x.le(9)));
console.log(`x > 0 & x < 9: ${await solver.check()}`);

const solver2 = new Z3.Solver();
solver2.add(Z3.And(x.ge(10), x.le(9)));
console.log(`x > 10 & x < 9: ${await solver2.check()}`);