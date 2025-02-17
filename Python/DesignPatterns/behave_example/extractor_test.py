from extractor import Extractor


def test_postcode():
    extractor = Extractor()
    assert extractor.postcode("BS1") is None
    assert extractor.postcode("BS1 1RT") == "BS1 1RT"
