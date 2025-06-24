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

# Make Cypress and Cucumber work together
npm uninstall @cucumber/cucumber  # don't work together
npm install cypress-cucumber-preprocessor --save-dev

# Run Cypress with Allure reports
npm run allure:clear
npm run cy:run
```

Files and folders:

* `cypress.config.js` -- Cypress configuration script
* `./cypress/e2e/spec.cy.js` -- Cypress test
* `./cypress/e2e/greeting.feature` -- Cucumber feature file tested by Cypress
* `./src` -- The app's source code