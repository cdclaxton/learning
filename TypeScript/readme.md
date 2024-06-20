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

# Compile the code
./node_modules/.bin/tsc

# Run the code with NodeJS
node dist/index.js

# One liner to compile and run the code
./node_modules/.bin/tsc && node dist/index.js
```

## Background

* TypeScript is **structually typed** (duck typed) as opposed to **nominally typed**

## Types

* `unknown`
* `any` -- makes a value work like it would in JS
* `number` -- e.g. `2_000_000`
* `bigint` -- e.g. `1234n`
* `boolean` -- `true` or `false`
* `string`
* `symbol` -- e.g. `let a: unique symbol = Symbol('a');`
* Object types: array, function, constructor
* `undefined` -- not yet assigned
* `null` -- absence of a value
* `void` -- return type of a function that doesn't explicitly return anything
* `never` -- type a function that runs forever or returns an exception

* **Type literal**: e.g. `let a: true = true;`
* **Index signature**: `[key: T]: U` -- any number of keys of type T with values of type U
* `?` denotes optional
* `readonly` marks fields as effectively a `const`
* **Type alias**: e.g. `type Age = number;`
* Type union: `|`
* Type intersection: `&`
* **Tuples** are an array of fixed length
    * `[string, ...string[]]` -- list of strings with at least one element
* **Enum**
    * String to string
    * String to number
    * Be careful with `const enums` from other code and use `preserveConstEnums` in the `tsconfig.json` file

## Functions
