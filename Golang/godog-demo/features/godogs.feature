Feature: eat godogs
    In order to be happy
    As a hungry gopher
    I need to be able to eat godogs

    Scenario: Eat 5 out of 12
        Given there are 12 godogs
        When I eat 5
        Then there should be 7 remaining
    
    Scenario Outline: Eat godogs
        Given there are 20 godogs
        When I eat <number>
        Then there should be <result> remaining
    
    Examples:
        | number | result |
        | 20     | 0      |
        | 10     | 10     |
        | 2      | 18     |