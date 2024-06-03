# JavaScript

## Install Node.js on Linux

```bash
sudo apt-get update
sudo apt-get upgrade

# Install Node.js
sudo apt-get install nodejs

# Check that Node.js was installed
node --version
```

## Introduction to JavaScript

Notes from:
* Mozilla Developer Network
* "Up and Going"
* "Rediscovering JavaScript: Master ES6, ES7, and ES8"

* JavaScript engines:
    - **SpiderMonkey** -- Mozilla Firefox
    - **v8** -- Chrome
    - **Node** -- built on v8 (run JavaScript outside of the browser)
* Engines compile the program on the fly and then immediately runs the compiled code
* Differentiation:
    * **ECMAScript** -- specification
    * **JavaScript** -- programming language
* Dynamic programming language (dynamic types)
* Case sensitive
* Statements end with a semicolon `;`
* Arrays are zero-based
* Doesn't support associative arrays (hashmaps or dicts)
* Semicolons are not optional
* Automatic Semicolon Insertion (ASI) -- therefore be careful with line breaks, especially near `break`, `continue`, `return`, `throw` or `yield`
* Polyfilling
    - take a definition of a new behaviour / feature and implement in an older version of JS
    - not all new features can be polyfilled (can't add newer syntax)
    - vetted polyfills in ES5-Shim and ES6-Shim
* Transpiling
    - converts newer code to older code equivalents
    - transforming + compiling
    - Babel transpiles ES6+ to ES5, Traceur transpiles ES6, ES7+ into ES5
* Code linters
    - Notable tools: JSLint, JSHint, ESLint
    - Installation:

```bash
npm install -g eslint
npm init
eslint --init
esline .
```

* `use strict` does not allow:
    - undeclared variables
    - changes to read-only properties
    - deletion of properties
    - deletion of variables and functions, e.g. `delete x;`
    - duplicate parameters in a function, e.g. `function f(p1,p1) {}`
    - octal numeric literals, e.g. `0120`


## Using JavaScript in HTML

* JavaScript must be inserted between `<script>` and `</script>` tags, e.g.

```html
<head>
    <script>
        // JavaScript goes here
        use strict;
    </script>
</head>
```

* Put the code in an external file and link with `<script src='myJavaScript.js'></script>`
* Put the code at the end of the `<body>` to improve load times    
* Can display data (e.g. for debugging) with:
    - `window.alert()` -- pop-up
    - `document.write()` -- write to document (deletes all if used after load)
    - `innerHTML` -- modify tag
    - `console.log()` -- browser console
* Events:
    - onchange
    - onclick
    - onmouseover
    - onmouseout
    - onkeydown
    - onload

## Comments

```js
// Single line comment
/* Multi-line comment */
```

## Variables

* Use camelCase notation
* Identifiers must start with letters, `_` or `$`
* Don't use `var` (old)
    - accidental global variable defined if `var` is missed (without `use strict`)
    - doesn't stop variables being redefined in a scope
    - does not have block scope (variable is hoisted)
    - protecting variables required Immediately Invoked Function Execution (IIFE)
* Data types
    - `String` -- literals surrounded by single or double quotes
    - `Number`
    - `Boolean` -- `true` or `false`
    - `Array` -- e.g. `let myVar = [1, 'Bob', true];`
    - `Object`
    - `null` / `undefined`
    - `symbol` -- new in ES6
* Type operators:
    - `typeof`
    - `instanceof`
* Define a variable with `let`:
    - doesn't allow redefinition
    - has block scope
    - not hoisted
* Define a constant with `const`:
    - immutable, therefore preferred
    - best to use if a function outside of the immediate scope has access
    - only primitive values and references to objects are protected from change (actual object doesn't receive any protection)
    - object properties of a `const` object are not constant
    - `Object.freeze()` makes the top-level properties constant
* Coerced into boolean false: 
    - "" (empty string)
    - 0, -0, NaN
    - null, undefined
    - false

## Scope

- **Global scope** -- top-level, accessible from everywhere in the code
- Variable declared outside of a function is global
- Assign a value to a variable that hasn't been declared, it becomes global (use strict mode to prevent this)
* Scope
    - **Lexical scope** -- scope where the variable is defined
    - **Dynamic scope** -- provided by the caller of the function

## Lexical scope

* Code in an inner scope can access variables in the outer scope
* Hoisting:
    - declaration is conceptually moved to the top of its enclosing scope
    - common and accepted to use hoisted function declarations, but not for variables

## Booleans

* Values `true` and `false`
* Operators:
    - `&&` and
    - `||` or
    - `!` not

### Logical comparison

| Symbol | Meaning                            |
|--------|------------------------------------|
| ==     | equal value (loose)                |
| ===    | equal value and type (strict)      |
| !=     |                                    |
| !===   | not equal value or not equal type  |
| >      |                                    |
| >=     |                                    |
| <      |                                    |
| <=     |                                    |
| ?      | ternary operator                   |

* `==` loose equality -- checks for value equality with coercion
* `===` strict equality -- checks for value equality without coercion
* For non-primative values (objects, functions, arrays, etc.), the values are held by reference, so both `==` and `===` will check whether the references match, i.e. not their values.

```js
[1,2,3] == "1,2,3"   // true
[1,2,3] === "1,2,3"  // false
[1,2,3] == [1,2,3]   // false
[1,2,3] === [1,2,3]  // false
```

## Type coercion

```js
// Explicit coercion to a number
Number("42")  

// Implicit coercion 
"42" == 42   // loosely equal (true)
"42" === 42  // strict equals (false)
```

## Numbers

| Symbol | Meaning        |
|--------|----------------|
| +      | addition       |
| -      | subtraction    |
| _      | separator      |
| /      | division       |
| *      | multiplication |
| %      | modulo         |
| ++     | increment      |
| --     | decrement      |
| =      | assignment     |
| +=     |                |
| -=     |                |
| /=     |                |
| %=     |                |

```js
2_000_000  // 2 million
```

## Symbol

* Primitive type
* Used to define the properties of a object (don't appear during normal iteration, but not private or encapsulated)
* Used to define special well-known methods in objects
* Defined with `Symbol(<name>)` but the `<name>` has no significance and each call creates a unique `Symbol`
* Symbol is unique, so it can be used to check if a class implements a specific method
* Many well-known Symbols, such as `Symbol.iterator`, `Symbol.match`, `Symbol.replace`, `Symbol.search`, etc.

## Destructuring

- Elegant way to extract data from arrays and objects
- Array destructuring -- use empty argument to ignore values, can set default values, can use 'rest', can be used to extract parameter values

## Prototypes

* **Prototypes** are the mechanism by which JavaScript objects inherit features
* JavaScript is a prototype-based language
* **Prototype object**
    - provides inheritance (acts as a template)
    - inherited methods and properties are defined on the `prototype` property
* **Prototype chain**
    - an object's prototype may also have a prototype object
    - methods and properties are not copied from one object to another, they are accessed by walking up the chain
    - look at `String.prototype` to see inherited methods and properties
* Methods added to a prototype are available to all object instances created from the constructor
* Common pattern:
    - define properties in the constructor
    - define methods on the prototype

## Functions

* Different ways to define a function:
    - Named function, e.g. `function foo(x) { ... }`
    - Anonymous function, e.g. `const foo = function(x) { ... }`
    - Arrow function, e.g. `const foo = (x) => { ... }` (no name, more concise than anonymous functions)
* Accessing the function without () will return the defined function
* Immediately Invoked Function Expression (IIFE)
    - Note that it is enclosed in `( ... )`
    - The final () executes the function
    - Often used to declare variables that won't affect the surrounding code outside of the IIFE

### Function arguments

* Number of arguments passed to a function:
    - too few => extra named parameters are `undefined`
    - too many => extra named parameters are ignored
* Rest parameter:
    - parameter name is preceded with `...`, e.g. `...values`
    - stands for the rest of the parameters
    - of type `Array`
    - has to be the last formal parameter 
    - can only be at most one rest parameter in a function's parameter list
    - only contains the values that have not been given an explicit name
    - gathers discrete values into an `Array`

### Default parameters

* Default parameters:
    - less work when calling a function if it has a sensible default
    - evolve a function signature without breaking backward compatibility
    - compensate for the lack of function overloading in JavaScript
    - keep all default parameters in the trailing position (although not enforced)
    - set a parameter to `undefined` to use the default value
    - can't give a default value to a 'rest' parameter
* Expressions as default parameters:
    - default values are not limited to literals
    - can't use a parameter that's to the right in the computation

### Arrow functions

* Arrow functions
    - Parenthesised parameter list (unless there's only one parameter)
    - Single-line body or compound multiline body surrounded by `{}`
    - Implicit `return` statement if no `{}`
    - Don't pass multiline arrow functions as function arguments -- messy
    - Have to use `()` if using a rest parameter
    - Can take default values

* Anonymous vs. Arrow functions
    - Anonymous functions -- all non-parameter, non-local variables are lexically scoped (except for `this` and `arguments` which use dynamic scoping)
    - Arrow functions -- consistent lexical scope for all non-parameter, non-local variables
    - Arrow functions can't be named, unlike 'anonymous' functions
    - Arrow functions can't be used as a constructor (use the new `class`)
    - Arrow functions can't be used as generators, need `function*(start) { ... }`
    - `throw` requires wrapping, e.g. `const crazy = () => { throw new Error("eek"); };`
    - returning an object literal needs `({ ... })`
    - Don't use arrow functions for registering event handlers if `this` needs dynamic scoping
    - Arrow functions are called lambda functions in other languages, like Python

### Functional style

* `bind()` function used to curry arguments to functions
    - to curry n parameters, n + 1 arguments are required (one is null)
    - first argument (null) binds to `this`

### Generators

- generates values (lazy evaluator)
- name must start with a `*`
- body should have one or more yields
- replace `*[Symbol.iterator]()` (as an iterator) with `*<name>()`
- have to call generator function directly (therefore, a class can have multiple generators)
- can be used to create an infinite stream

### Iterators

- Built-in collections (such as Array, Set, Map) are iterable
- Implements a function named `[Symbol.iterate]()`

### Closures

* Way to remember and continue to use a function's scope (variables) once the function has finished running

## Modules

* Module pattern uses functions
* Define private implementation details (functions, variables)
* Define public API
* Modules
    - well-encapsulated, single file that contains variables, constants, functions and classes
    - imports specify what is needed (can't use what hasn't been imported), usually placed at the top of the file
    - exports specify what is provided to others (everything else is hidden)
    - code is automatically executed in strict mode
    - NodeJS requires modules to have the extension .mjs
    - a module is only loaded once
    - imports don't need file extension, e.g. `import { right } from './right'`
    - import path should be a relative path, absolute path or the name of the module file
    - to import a reference as a different name: `import { Thermostat as HomeThermostat } from './home';`
    - to import into a namespace `home` use `import * as home from './home';` (ignore the default export)
    - to just run (side effects) code in a module and not import anything `import 'name';`
    - to run: `node --experimental-modules left.mjs`
* Inlining exports (preferred method)
    - declare the reference or the class at the same time as exporting it, e.g. `export const FREEZING_POINT = 0;`
* Explicit exports
    - e.g. `export { c2f, FREEZING_POINT }`
    - to export with a different name: `export { c2k as celsiusToKelvin }`

* Default exports
    - a module can only have one default export
    - signifies a major export from the module
    - e.g. `export default function x() { ... }`  can only be used for functions and classes

* Rexporting from another module
    - to rexport everything (except default) from a module `export * from './temperature';` 
    - to rexport selected references `export { Thermostat, celsiusToKelvin } from './temperature';`
    - to export with a different name `export { Thermostat as Thermo, default as default } from './temperature';`

## Asynchronous

* Most functions in JavaScript libraries are asynchronous
* Promises replace callbacks (traditional approach)
* Promises are non-blocking and will return either a result or an error
* Promise = object through which a function can propagate an error or a result sometime in the future
* Promise states:
    - pending -- asynchronous function hasn't completed
    - resolved -- completed successfully
    - rejected -- error
* `.then()` function -- used to receive and process data (returns another instance of the promise)
* `.catch()` function -- used to receive and process an error
* can't explicitly query a Promise for its state
* The 'Bluebird' library can be used to wrap callbacks in promises

* Working with multiple promises:
    - `Promise.race()` -- takes an array of promises and returns the first one to resolve or reject
    - `Promise.all()` -- takes an array of promises and passes an array of resolved results to the `then()` function when all promises resolve (if any of the promises is rejected, then `catch()` function is called)
* `async` -- use an asynchronous function as if it were synchronous
* `await` -- call an asynchronous function as it if it were synchronous (can only be used with functions marked `async`)

## Fetching data from the server

* `fetch()` method returns a promise
* `response.text` returns a promise

```javascript
fetch(url).then(function(response) {
  response.text().then(function(text) {
    // do something with the text
  });
});
```

* the above is equivalent to:

```javascript
fetch(url).then(function(response) {
  return response.text()
}).then(function(text) {
  // do something with the text
});
```

## Client-side storage

* **Cookies** 
    - used to store information or personalise websites
    - outdated, have security problems, can't store complex data
    - supported by extremely old browsers
* **Web storage API**
* **IndexedDB API**