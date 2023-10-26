Feature: Calculate probability of a sequence

    Scenario: There are no tokens missing
        Given there are 5 tokens present
        And there are 0 tokens missing
        And the probability of a missing token is 0
        When I calculate the probability
        Then the occurrence probability should be 1.0
    
    Scenario Outline: There are tokens missing
        Given there are 5 tokens present
        And there are <number> tokens missing
        And the probability of a missing token is 0.1
        When I calculate the probability
        Then the occurrence probability should be <result>
    
    Examples:
        | number | result   |
        | 0      | 0.590490 |
        | 1      | 0.059049 |