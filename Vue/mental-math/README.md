# mental-math

Simple mental maths tester application built using Vue.js and TypeScript.

Colour scheme from: https://www.schemecolor.com/energetic-vibrant.php

## Setup

```bash
# Install the required dependencies
npm install

# Run the unit tests
npm run test:unit

# Run a dev version (hotloads)
npm run dev
```

## Design

To run the design's `index.html`, right-click the file in VS Code and select `Open with Live Server`.

## Deploy to website

```bash
# Build the app and place in a folder called 'dist'
npm run build

# Copy the built app to the website
rm -rf ~/website/mental-math/
mkdir ~/website/mental-math/
cp -r ./dist/* ~/website/mental-math/
```
