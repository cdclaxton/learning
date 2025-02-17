Feature: Postcode extraction

    Scenario: No postcode present in text
        Given we have a postcode extractor
        When we send "BS1"
        Then it won't return anything

    Scenario: Single postcode present in text
        Given we have a postcode extractor
        When we send "BS1 1RT"
        Then it will return "BS1 1RT"

    Scenario Outline: Multiple postcodes
        Given we have a postcode extractor
        When we send <input>
        Then it will return <output>

        Examples:
            | input   | output  |
            | BS1     |         |
            | BS1 1RT | BS1 1RT |

    Scenario: Table of data to extract
        Given a table
            | ID | Text             |
            | 1  | Seen at BS1 1RT  |
            | 2  | Unknown postcode |

        When we extract postcodes in a table
        Then we get
            | ID | Text             | Result  |
            | 1  | Seen at BS1 1RT  | BS1 1RT |
            | 2  | Unknown postcode |         |
