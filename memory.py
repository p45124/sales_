"""Session memory and NPC relationship tracking."""

from dataclasses import dataclass, field


@dataclass
class Memory:
    """Stores session summaries and NPC trust levels."""

    summaries: list[str] = field(default_factory=list)
    npc_trust: dict[str, int] = field(default_factory=dict)

    def update_summary(self, text: str) -> None:
        """Append a summary of the latest event."""
        self.summaries.append(text)

    def adjust_trust(self, npc_name: str, delta: int) -> int:
        """Adjust and return the NPC's trust level."""
        current = self.npc_trust.get(npc_name, 0)
        current += delta
        self.npc_trust[npc_name] = current
        return current

    def npc_state(self, npc_name: str) -> str:
        """Return a string describing the NPC trust level."""
        trust = self.npc_trust.get(npc_name, 0)
        return f"{npc_name} trust level: {trust}"
