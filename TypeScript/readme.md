# TypeScript

## Install

```bash
sudo apt-get install nodejs npm
```

## Start a new project

```bash
mkdir demo
cd demo

# Initialise a new NPM project
npm init

# Install the TypeScript compiler (TSC), linter and type declarations
npm install --save-dev typescript tslint @types/node

# Create the tsconfig.json file (should be in the root directory of the project)
./node_modules/.bin/tsc --init

# Create the tslint.json file
./node_modules/.bin/tslint --init

# Create a src directory and the index.ts file
mdkir src
touch src/index.ts

# Edit index.ts

# Compile and run the from the demo directory
./node_modules/.bin/tsc && node dist/index.js
```

## Background

* TypeScript is **structually typed** (duck typed) as opposed to **nominally typed**

## Types

* `unknown` -- can't use a value of type unknown until it has been refined by checking what it is
* `any` -- makes a value work like it would in JS
* `number` -- set of all numbers (integers, floats, Infinity, NaN), e.g. `2_000_000`
* `bigint` -- e.g. `1234n`
* `boolean` -- `true` or `false`
* `string`
* `symbol` -- e.g. `let a: unique symbol = Symbol('a');`
* Object types: array types, function types, constructor types
* `undefined` -- not yet assigned
* `null` -- absence of a value
* `void` -- return type of a function that doesn't explicitly return anything
* `never` -- type of a function that runs forever or returns an exception
    - subtype of every other type

* **Type literal**: a type that represents a single value, e.g. `let a: true = true;`

* Objects:
    * **Index signature**: `[key: T]: U` -- any number of keys of type T with values of type U (type must be assignable to a number or string)
    * `?` denotes optional
    * `readonly` marks fields as effectively a `const`
    * Use object literal notation (shape) or `object` (avoid `Object`)
* **Type alias**
    - e.g. `type Age = number;`
    - never inferred by TypeScript
* Type union: `|`
    - a value with a union type can be both members at once
* Type intersection: `&`
* **Arrays**:
    - e.g. `number[]` or `Array<number>`
    - once an array leaves the scope in which it was defined, TypeScriptv will assign it a final type (that can't be expanded)
    - read-only arrays can't be updated in place (can't use `.push` and `.splice`)
    - `readonly string[]`
    - `ReadonlyArray<string>`
    - `Readonly<string[]>`
* **Tuples** are an array of fixed length
    * sub-type of array
    * `[number, number?]` -- tuple with one or two elements
    * `[string, ...string[]]` -- list of strings with at least one element
    * `readonly [number, string]`
    * `Readonly<[number, string]>`
* **Enum**
    * Enumerate the possible values for a type
    * Maps keys to values
    * Two types of enums:
        * String to string
        * String to number
    * Access a value with dot or bracket notation, e.g. `Language.Russian` or `Language['Russian]`
    * Be careful with `const enums` from other code and use `preserveConstEnums` in the `tsconfig.json` file (as the enum's value is inlined)
    * Use `const enums` with string values as numbers are assignable to enums

## Functions

* Generally, parameters should be explictly annotated
* Return types can be annotated, but they will be inferred
* **Parameter** = declared as part of the function definition
* **Argument** = data passed to a function when invoking it
* Mark optional parameters with `?`
* Default parameters, e.g. `a: number = 10`
* Variadic: `...numbers: number[]` (rest parameter has to be last and a function can only have one)
* A parameter named `this` is a reserved word
* Generator function:
    - produces a stream of values
    - `function* <name>(<parameters>)`
    - `yield` keyword to yield values
* Iterator:
    - consumes values from a generator
* `Function` is the type of a function (catchall for all functions)
* Syntax for a function type (call signature or type signature):
    - shorthand, e.g. `type Adder = (a: number, b: number) => number`
    - full, e.g. `type Adder = { (a: number, b: number): number }`
    - parameter names are just documentation
    - cannot express default values
    - can bind to type aliases, e.g. `type Greet = (name: string) => string`
* Overloaded function has multiple call signatures
* In JavaScript, functions are callable objects so properties can be assigned to them
* Generic type parameter = polymorphic type parameter
* Bounded polymorphism: `<T extends SuperType>`
* Generic types can have defaults

## Classes and interfaces

* `class <name> {}`
* `class <name> extends <super class> {}`
* Access modifiers:
    * `public` -- default access level
    * `protected` -- accessible from instances of this class and subclasses
    * `private` -- accessible from instances of this class only
* Abstract class:
    * `abstract class <name> {}`
    * can have abstract methods and properties
* `static` methods
* `readonly` instance properties
* `super.<name>` to call super class method
* `super()` from the constructor method to call the super class' constructor method
* `this` is also a return type
* Interfaces:
    * can extend other interfaces, an object type, or a class
    * declaration merging occurs automatically
    * `class <name> implements <interface> {}`
    * can declare instance properties (which can be marked as `readonly`), but can't declare visibility modifiers
    * a class can implement multiple interfaces
* Polymorphism:
    * a generic can be scoped to a whole class or to specific methods
    * static methods don't have access to their class' generics
* Mixins:
    * simulate multiple inheritance
    * for role-orientated programming
* Final classes:
    * TypeScript doesn't support the `final` keyword
    * To simulate a final class, make the constructor `private` and add a static method that calls the private constructor

## Advanced types