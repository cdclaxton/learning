# Cucumber tests (BDD)

* Behaviour Driven Development (BDD)
* Aids collaboration between business and technical teams, thus improving communication
* Builds a common understanding of the behaviour of the application
* Generates common (living) documentation that can be understood by the teams and stakeholders (generating a single source of truth)
* Stages:
    * Discovery -- explore and discuss how the system should behave. This may involve the 3 amigos (product owner, developers and testers).
    * Formulation -- create concrete examples that can be automated
    * Automation -- coding to implement the agreed system behaviour
* Use a ubiquitous language (from Domain Driven Development)
* The separation of the tests from the code is robust and allows the underlying system to be recoded (e.g. in a different language), but the tests remain the same.
* Gherkin specification language keywords:
    * `Feature` -- high-level description of a software feature. There can only be one `Feature` in a `.feature` file.
    * `Rule` -- used to group together several scenarios that belong to a business rule
    * `Example` -- concrete example (with steps) that illustrates a business rule (synonym for `Scenario`)
    * `Examples`
    * `Scenario`
    * `Scenarios`
    * `Background` -- add context to the scenarios that follow it; can contain one or more `Given` steps that are un before each scenario
    * `Scenario Outline` -- used to run the same `Scenario` multiple times with different combinations of values; must contain one or more `Examples`; steps can use `<>` delimited parameters that reference headers in the examples table
    * `Scenario Template` -- synonym of `Scenario Outline`
    * `Data Tables` -- passed to the step function as the last argument
    * Steps (note that keywords are not taken into account when looking for a step definition):
        * `Given` -- precondition or initial context to put the system into a known state
        * `When` -- action or event
        * `And` -- repeats the previous type of step
        * `But` -- repeats the previous type of step
        * `Then` -- expected outcome (the step definition should use an assertion to compare the actual outcome to the expected outcome)
        * `*` -- can be used in place of any normal step keywords (use to show a list)
    * `"""` - doc strings for passing larger pieces of text to a step definition (or three backticks)
    * `|` -- data tables
    * `@` -- tag (placed above a `Feature` to group related features)
    * `#` -- comment (only permitted at the start of a new line)

To run the tests:

```bash
go test .
```


