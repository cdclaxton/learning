from loyalty import LoyaltyMember, LoyaltyScheme


def test_loyalty_member():
    member = LoyaltyMember("Bob", b'123', 10)
    assert member.name == "Bob"
    assert member.barcode == b'123'
    assert member.points == 10
    
    member.add_points(20)
    assert member.points == 30


def test_loyalty_scheme():
    scheme = LoyaltyScheme([])
    assert scheme.get_member("Bob") is None

    member1 = LoyaltyMember("Bob", b'123', 10)
    member2 = LoyaltyMember("Sarah", b'456', 10)
    scheme = LoyaltyScheme([member1, member2])
    assert scheme.get_member(b'123') == member1
    assert scheme.get_member(b'456') == member2