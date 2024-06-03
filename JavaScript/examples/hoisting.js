let a = 2;

// works because foo() is hoisted
foo();

function foo() {
    
    console.log(`a: ${a}`);

    // Hoisting a variable doesn't work:
    // ReferenceError: Cannot access 'b' before initialization
    // b = 3;
    // let b;
    // console.log(`b: ${b}`);
}