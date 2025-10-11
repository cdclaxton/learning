# Different ways to style React components

## Setup and run the app

```
npm install
npm run start
```

## Styles

* Inline CSS: The `Header` component uses inline CSS. Note that the CSS style `padding-left` becomes `paddingLeft` when defined in a JS/TS object. Adding styling for 'hover' for an HTML button requires using `onMouseEnter` and `onMouseLeave` events and state and so a button was created as its own React component.

* Normal CSS: The `Information` component uses CSS defined in a separate CSS file.

* `react-jss` library: The `Result` component uses the `react-jss` library. It is similar to using inline CSS.