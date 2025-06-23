# Cypress and Cucumber tests

The code in this repo explores how to use the Cypress test framework with Cucumber tests.

The commands used during the construction of the code base are as follows.

```bash
# Start a new NodeJS project
npm init

# Install Cypress as a dev dependency
npm install cypress --save-dev

# Run the Cypress executable
npx cypress open
npm run cy:open  # defined in package.json

# Install Cucumber
npm install @cucumber/cucumber --save-dev

# Run the Cucumber tests
npx cucumber-js
```

Files and folders:

* `cypress.config.js` -- Cypress configuration script
* `./cypress/e2e/spec.cy.js` -- Cypress test
* `./features` -- Cucumber test foldee
* `./features/*.feature` -- Feature file tests in Gherkin syntax
* `./features/support/*.js` -- JS code to run feature tests
* `./src` -- The app's source code