"""Dice rolling utilities."""

from random import randint


def roll_die(sides: int) -> int:
    """Roll a die with the given number of sides and print the result."""
    result = randint(1, sides)
    print(f"[Dice] d{sides} roll: {result}")
    return result


def roll_d20() -> int:
    """Roll a d20."""
    return roll_die(20)


def roll_d6() -> int:
    """Roll a d6."""
    return roll_die(6)
