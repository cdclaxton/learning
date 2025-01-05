# Scenario Consequences

Vue-based web-app to calculate probability distributions.

![Screenshot](./design/Screenshot.png)

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Design

The class structure is shown in the UML class diagram below.

![Class diagram](./design/design-Class%20diagram.drawio.png)

The events emitted by the components and the handler functions are shown in the diagram below.

![Event diagram](./design/design-Events.drawio.png)

### Vue.js crib sheet

![Vue.js crib sheet](./design/design-Crib%20sheet.drawio.png)

## Build and upload to website

```bash
# Build the app and place in a folder called 'dist'
npm run build

# Copy the built app to the website
cp -r ./dist/* ~/website/scenario-consequences/
```
