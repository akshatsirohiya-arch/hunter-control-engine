# engine/permissions.py
# Defines allowed actions based on damage score

def get_regime(damage_score):
    if damage_score <= 1:
        return "NORMAL"
    elif damage_score <= 3:
        return "DAMAGED"
    elif damage_score <= 5:
        return "SEVERE"
    else:
        return "CRISIS"


def get_permissions(damage_score):
    if damage_score <= 1:
        return {
            "Hunter capital": "25%",
            "Initial position size": "1%",
            "Max positions": "8–10",
            "Adds to winners": "Allowed"
        }

    elif damage_score <= 3:
        return {
            "Hunter capital": "15%",
            "Initial position size": "0.5%",
            "Max positions": "4–5",
            "Adds to winners": "Restricted"
        }

    elif damage_score <= 5:
        return {
            "Hunter capital": "5–10%",
            "Initial position size": "0.25–0.5%",
            "Max positions": "1–2",
            "Adds to winners": "Not allowed"
        }

    else:
        return {
            "Hunter system": "OFF",
            "Action": "Capital preservation only"
        }
