Feature: Standardising sort codes

    Scenario Outline: standardise sort codes
        Given a sort code standardiser
        When I standardise <sort_code>
        Then it returns <expected_sort_code>

        Examples:
            | sort_code  | expected_sort_code |
            | 102030     | 102030             |
            | 10 30 40   | 103040             |
            | 10-20-50   | 102050             |
            | "  102060" | 102060             |
            | "20-30-20" | 203020             |