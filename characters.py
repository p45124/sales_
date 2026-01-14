"""Character definitions and player creation logic."""

from dataclasses import dataclass, field


CLASS_STATS = {
    "Warrior": {"max_hp": 20, "attack": 5, "defense": 3},
    "Mage": {"max_hp": 14, "attack": 7, "defense": 1},
    "Rogue": {"max_hp": 16, "attack": 6, "defense": 2},
}


@dataclass
class Character:
    """Represents a player character."""

    name: str
    class_name: str
    max_hp: int
    hp: int
    attack: int
    defense: int
    inventory: list[str] = field(default_factory=list)
    xp: int = 0

    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        """Apply damage and return actual damage dealt."""
        actual = max(0, damage)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount: int) -> None:
        """Heal the character by a given amount."""
        self.hp = min(self.max_hp, self.hp + amount)


def create_character(name: str, class_name: str) -> Character:
    """Create a character from class presets."""
    stats = CLASS_STATS[class_name]
    return Character(
        name=name,
        class_name=class_name,
        max_hp=stats["max_hp"],
        hp=stats["max_hp"],
        attack=stats["attack"],
        defense=stats["defense"],
    )
