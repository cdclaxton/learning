Feature: Amend contact list

    Background: Initial contacts
        Given there are contacts:
            | name | phone number |
            | Bob  | 1234         |
            | Jane | 4566         |

    Scenario: Get a contact
        When I get the contact Bob
        Then the phone number should be 1234

    Scenario: Add a contact
        When I add the contact Bill with number 6789
        Then the contacts should be:
            | name | phone number |
            | Bill | 6789         |
            | Bob  | 1234         |
            | Jane | 4566         |
    
    Scenario: Remove a contact
        When I remove the contact for Bob
        Then the contacts should be:
            | name | phone number |
            | Jane | 4566         |

    Scenario: Add two contacts
        When I add the contact Bill with number 6789
        And I add the contact Sally with number 0987
        Then the contacts should be:
            | name  | phone number |
            | Bill  | 6789         |
            | Bob   | 1234         |
            | Jane  | 4566         |
            | Sally | 0987         |