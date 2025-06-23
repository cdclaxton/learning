const { When, Then } = require('@badeball/cypress-cucumber-preprocessor');
const { Greeter } = require("../../src/index")

When('the greeter says hello', function() {
    this.whatIHeard = new Greeter().sayHello();
});

Then('I should have heard {string}', function(expectedResponse) {
    assert.equal(this.whatIHeard, expectedResponse);
});