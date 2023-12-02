# Unit tests for regex_extract.py


from regex_extract import extract


def test_no_entities():
    text = "This doesn't contain an account."
    assert extract(text) == []


def test_one_entity():
    text = "01-02-03 12345678"
    assert extract(text) == [{"account": "12345678", "sortcode": "01-02-03"}]


def test_one_entity_surrounding_text():
    text = "Please transfer £10 to 01-02-03 12345678 by Friday."
    assert extract(text) == [{"account": "12345678", "sortcode": "01-02-03"}]


def test_two_entities():
    text = "Accounts: 01-02-03 12345678 and 89-90-91 09876543."
    assert extract(text) == [
        {"account": "12345678", "sortcode": "01-02-03"},
        {"account": "09876543", "sortcode": "89-90-91"},
    ]
