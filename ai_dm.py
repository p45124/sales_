"""AI Dungeon Master narration logic."""


def narrate(payload: dict) -> str:
    """Return narration text based on structured engine input.

    Expected payload keys:
    - scene
    - player_action
    - dice_result
    - engine_outcome
    - npc_state
    """
    scene = payload.get("scene", "")
    action = payload.get("player_action", "")
    outcome = payload.get("engine_outcome", "")
    npc_state = payload.get("npc_state", "")

    lines = [scene, f"You choose to {action}.", outcome]
    if npc_state:
        lines.append(npc_state)
    return " ".join(line for line in lines if line)
