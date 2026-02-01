# main.py
# Runs the Hunter Control Engine

from engine.score import compute_damage_score
from engine.permissions import get_regime, get_permissions


def run():
    # Temporary manual inputs (will automate later)
    from engine.data_fetch import get_breadth_percent
breadth_percent = get_breadth_percent()

    from engine.data_fetch import get_vix_change_pct
vix_change_pct = get_vix_change_pct()


    damage_score = compute_damage_score(
        breadth_percent=breadth_percent,
        vix_change_pct=vix_change_pct
    )

    regime = get_regime(damage_score)
    permissions = get_permissions(damage_score)

    print("\n=== HUNTER CONTROL ENGINE ===")
    print(f"Damage Score: {damage_score} / 6")
    print(f"Market Regime: {regime}")
    print("\nPermissions:")
    for k, v in permissions.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    run()
