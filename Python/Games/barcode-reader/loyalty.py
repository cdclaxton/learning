from dataclasses import dataclass

@dataclass
class LoyaltyMember:
    """Loyalty card member."""
    name: str # member's name
    barcode: bytes  # unique barcode for the member
    points: int # accrued loyalty points

    def add_points(self, points: int) -> None:
        """Add loyalty points for the member."""
        assert points >= 0
        self.points += points


class LoyaltyScheme:
    """Loyalty scheme engine."""
    
    def __init__(self, members: list[LoyaltyMember]):
        # Store the members as a dict of their barcode to the member for quick lookup
        self._members = {member.barcode: member for member in members}
    
    def get_member(self, barcode: bytes) -> LoyaltyMember|None:
        return self._members.get(barcode, None)
