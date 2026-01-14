"""Core game rules and action resolution."""

from dataclasses import dataclass

from dice import roll_d20, roll_d6
from memory import Memory
from characters import Character


@dataclass
class Enemy:
    """Represents an enemy in the encounter."""

    name: str
    hp: int
    attack: int
    defense: int

    def is_alive(self) -> bool:
        """Check if the enemy is still alive."""
        return self.hp > 0


@dataclass
class EngineResult:
    """Result of an engine action."""

    scene: str
    player_action: str
    dice_result: str
    outcome: str
    npc_state: str = ""


class GameEngine:
    """Deterministic game engine for resolving actions."""

    def __init__(self, players: list[Character], memory: Memory) -> None:
        self.players = players
        self.memory = memory
        self.enemy = Enemy(name="Goblin Raider", hp=18, attack=4, defense=1)
        self.quest_complete = False

    def current_scene(self) -> str:
        """Return a brief description of the current scene."""
        if self.enemy.is_alive():
            return "A goblin raider blocks the forest path, gripping a jagged blade."
        return "The forest path is clear, moonlight spilling onto the road ahead."

    def resolve_action(self, player: Character, action: str) -> EngineResult:
        """Resolve a player action and return the structured result."""
        action = action.lower()
        if action == "attack":
            return self._resolve_attack(player)
        if action == "talk":
            return self._resolve_talk(player)
        if action == "explore":
            return self._resolve_explore(player)
        return EngineResult(
            scene=self.current_scene(),
            player_action=action,
            dice_result="None",
            outcome="You hesitate, unsure what to do next.",
        )

    def _resolve_attack(self, player: Character) -> EngineResult:
        scene = self.current_scene()
        if not self.enemy.is_alive():
            return EngineResult(
                scene=scene,
                player_action="attack",
                dice_result="None",
                outcome="There is nothing left to strike.",
            )
        roll = roll_d20()
        dice_result = f"d20={roll}"
        if roll + player.attack >= 10 + self.enemy.defense:
            damage_roll = roll_d6()
            damage = max(1, damage_roll + player.attack - self.enemy.defense)
            self.enemy.hp = max(0, self.enemy.hp - damage)
            outcome = (
                f"Your strike lands true, dealing {damage} damage. "
                f"Enemy HP is now {self.enemy.hp}."
            )
            if not self.enemy.is_alive():
                player.xp += 10
                self.quest_complete = True
                outcome += " The goblin collapses, and the path is yours."
        else:
            outcome = "Your blow misses, the goblin ducking away."
        return EngineResult(
            scene=scene,
            player_action="attack",
            dice_result=dice_result,
            outcome=outcome,
        )

    def _resolve_talk(self, player: Character) -> EngineResult:
        scene = self.current_scene()
        roll = roll_d20()
        dice_result = f"d20={roll}"
        trust_delta = 1 if roll >= 12 else -1
        trust = self.memory.adjust_trust("Goblin Raider", trust_delta)
        if trust_delta > 0:
            outcome = (
                "Your calm words seem to reach the goblin. "
                "It lowers its weapon, listening."
            )
        else:
            outcome = (
                "Your words fall flat. The goblin snarls, "
                "tightening its grip."
            )
        npc_state = self.memory.npc_state("Goblin Raider")
        if trust >= 2:
            self.quest_complete = True
            outcome += " The goblin steps aside, allowing safe passage."
        return EngineResult(
            scene=scene,
            player_action="talk",
            dice_result=dice_result,
            outcome=outcome,
            npc_state=npc_state,
        )

    def _resolve_explore(self, player: Character) -> EngineResult:
        scene = self.current_scene()
        roll = roll_d20()
        dice_result = f"d20={roll}"
        if roll >= 15:
            player.heal(2)
            outcome = "You find a calming herb and regain 2 HP."
        else:
            outcome = "You find only rustling leaves and distant owl calls."
        return EngineResult(
            scene=scene,
            player_action="explore",
            dice_result=dice_result,
            outcome=outcome,
        )

    def enemy_turn(self) -> list[str]:
        """Enemy attacks the first alive player."""
        if not self.enemy.is_alive():
            return []
        targets = [player for player in self.players if player.is_alive()]
        if not targets:
            return []
        target = targets[0]
        roll = roll_d20()
        if roll + self.enemy.attack >= 10 + target.defense:
            damage_roll = roll_d6()
            damage = max(1, damage_roll + self.enemy.attack - target.defense)
            dealt = target.take_damage(damage)
            return [
                f"The goblin slashes {target.name} for {dealt} damage."
            ]
        return [f"The goblin swings at {target.name} but misses."]

    def party_defeated(self) -> bool:
        """Check if all players are at 0 HP."""
        return all(not player.is_alive() for player in self.players)
