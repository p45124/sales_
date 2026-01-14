"""Main game loop for the pass-and-play RPG."""

from ai_dm import narrate
from characters import CLASS_STATS, create_character
from engine import GameEngine
from memory import Memory


def prompt_player_count() -> int:
    """Prompt for the number of players."""
    while True:
        try:
            count = int(input("Number of players (2-4): "))
        except ValueError:
            print("Please enter a number.")
            continue
        if 2 <= count <= 4:
            return count
        print("Please choose between 2 and 4 players.")


def prompt_class() -> str:
    """Prompt for a character class."""
    classes = ", ".join(CLASS_STATS.keys())
    while True:
        class_name = input(f"Choose class ({classes}): ").strip().title()
        if class_name in CLASS_STATS:
            return class_name
        print("Invalid class choice.")


def create_players() -> list:
    """Create player characters."""
    players = []
    for idx in range(prompt_player_count()):
        print(f"\n-- Player {idx + 1} setup --")
        name = input("Name: ").strip() or f"Player {idx + 1}"
        class_name = prompt_class()
        players.append(create_character(name, class_name))
    return players


def choose_action(player_name: str) -> str:
    """Prompt the player for an action."""
    actions = ["attack", "talk", "explore"]
    while True:
        choice = input(
            f"{player_name}, choose action (attack/talk/explore): "
        ).strip().lower()
        if choice in actions:
            return choice
        print("Invalid action.")


def print_status(players: list) -> None:
    """Print a quick party status."""
    print("\nParty Status:")
    for player in players:
        status = "Alive" if player.is_alive() else "Down"
        print(f"- {player.name} ({player.class_name}): {player.hp}/{player.max_hp} HP [{status}]")


def main() -> None:
    """Run the game loop."""
    print("Welcome to the AI Dungeon Master RPG!\n")
    players = create_players()
    memory = Memory()
    engine = GameEngine(players, memory)

    intro_payload = {
        "scene": "A misty forest road stretches ahead as danger stirs nearby.",
        "player_action": "gather your party",
        "dice_result": "",
        "engine_outcome": "The air is tense, and the night whispers of trouble.",
        "npc_state": "",
    }
    print("\n" + narrate(intro_payload))

    current_index = 0
    while not engine.quest_complete and not engine.party_defeated():
        player = players[current_index]
        if not player.is_alive():
            current_index = (current_index + 1) % len(players)
            continue
        print("\n" + "=" * 40)
        print_status(players)
        print("\nPass the device to the next player.")
        input("Press Enter when ready...")
        action = choose_action(player.name)
        result = engine.resolve_action(player, action)
        memory.update_summary(result.outcome)
        narration = narrate(
            {
                "scene": result.scene,
                "player_action": result.player_action,
                "dice_result": result.dice_result,
                "engine_outcome": result.outcome,
                "npc_state": result.npc_state,
            }
        )
        print("\n" + narration)

        for enemy_line in engine.enemy_turn():
            print(enemy_line)

        current_index = (current_index + 1) % len(players)

    print("\n" + "=" * 40)
    if engine.quest_complete:
        print("Quest complete! The party succeeds.")
    else:
        print("The party has fallen. The quest ends here.")


if __name__ == "__main__":
    main()

# Example gameplay output:
# Welcome to the AI Dungeon Master RPG!
#
# -- Player 1 setup --
# Name: Aria
# Choose class (Warrior, Mage, Rogue): Mage
#
# -- Player 2 setup --
# Name: Bram
# Choose class (Warrior, Mage, Rogue): Warrior
#
# A misty forest road stretches ahead as danger stirs nearby. You choose to gather your party. The air is tense, and the night whispers of trouble.
#
# ========================================
# Party Status:
# - Aria (Mage): 14/14 HP [Alive]
# - Bram (Warrior): 20/20 HP [Alive]
#
# Pass the device to the next player.
# Press Enter when ready...
# Aria, choose action (attack/talk/explore): attack
# [Dice] d20 roll: 16
# [Dice] d6 roll: 4
#
# A goblin raider blocks the forest path, gripping a jagged blade. You choose to attack. Your strike lands true, dealing 10 damage. Enemy HP is now 8.
# The goblin swings at Aria but misses.
