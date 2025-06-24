const { defineConfig } = require("cypress");
const createBundler = require("@bahmutov/cypress-esbuild-preprocessor");
const { addCucumberPreprocessorPlugin } = require("@badeball/cypress-cucumber-preprocessor");
const { createEsbuildPlugin} = require("@badeball/cypress-cucumber-preprocessor/esbuild");
const allureWriter = require("@shelex/cypress-allure-plugin/writer");

const fs = require("fs");
const path = require("path");
const Gherkin = require('@cucumber/gherkin');
const Messages = require('@cucumber/messages');

async function setupNodeEvents(on, config) {
  await addCucumberPreprocessorPlugin(on, config);

  on("file:preprocessor", createBundler({
    plugins: [createEsbuildPlugin(config)],
  }))

  allureWriter(on, config);

  return config;
}

function walkSync(dir) {
  console.log(`Walking directory: ${dir} ...`);

  let filepaths = []
  const directory = fs.opendirSync(dir);
  while (1) {
    const ret = directory.readSync();
    if (!ret) {
      break;
    }

    const entry = path.join(dir, ret.name);
    if (ret.isDirectory()) {
      filepaths.push(...walkSync(entry));
    } else if (path.extname(ret.name) === '.feature') {
      filepaths.push(entry);
    }
  }

  return filepaths;
}

function removeAtSymbolPrefix(name) {
  if (name.startsWith("@")) {
    return name.substring(1, name.length);
  }
  return name;
}

function getTagsFromFile(filepath) {

    // Read the file
    const fileContent = fs.readFileSync(filepath).toString();

    // Parse the file
    let uuidFn = Messages.IdGenerator.uuid();
    let builder = new Gherkin.AstBuilder(uuidFn);
    let matcher = new Gherkin.GherkinClassicTokenMatcher();

    let parser = new Gherkin.Parser(builder, matcher);
    let gherkinDocument = parser.parse(fileContent);

    // Extract the tags
    const tags = gherkinDocument.feature.tags;
    return tags.map(obj => removeAtSymbolPrefix(obj.name));
}

function getTags(dir) {

  console.log(`Getting tags from: ${dir}`);
  const result = {}
  for (const p of walkSync(dir)) {
    console.log(`Found .feature file: ${p}`);
    result[p] = getTagsFromFile(p);
    console.log(`Tags for ${p}: ${result[p]}`);
  }

  console.log("Result of getTags(): ");
  console.log(result);
  return result;
}

module.exports = defineConfig({
  e2e: {
    specPattern: ["**/*.feature", "**/*.cy.js"],
    setupNodeEvents,
  },
  env: {
    allureReuseAfterSpec: true,
  },
  featureFileTags: getTags("./cypress/e2e/"),
});

