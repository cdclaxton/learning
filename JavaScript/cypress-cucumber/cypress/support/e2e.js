// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';
import '@shelex/cypress-allure-plugin';

// Only process .feature files
if (Cypress.spec.fileExtension === '.feature') {
    console.log(`Found feature file: ${Cypress.spec.absolute}`)

    // Get the tags from the feature file
    console.log(Cypress.config().featureFileTags);
    const featureFileTags = Cypress.config().featureFileTags;

    // Find the tag(s) that match the feature file
    const matchingFilepaths = Object.keys(featureFileTags)
        .filter(filepath => Cypress.spec.absolute.endsWith(filepath))
    if (matchingFilepaths.length === 1) {
        const tags = featureFileTags[matchingFilepaths[0]];
        console.log(`Tag for ${Cypress.spec.absolute} = ${tags}`)

        Cypress.Allure.reporter.getInterface().epic(tags[0]);
        Cypress.Allure.reporter.getInterface().suite('Cat');
    }
}

