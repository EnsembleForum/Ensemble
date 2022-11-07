"""
Simple script to generate permissions.json file, in order to improve efficiency
"""
import json
import _helpers
from backend.models.permissions import Permission
del _helpers


output: dict[str, dict] = {}

for p in Permission:
    output[str(p.value)] = {
        "name": p.name,
        # FIXME: This doesn't return the right info - it looks like we can't
        # access individual docs for members of the enum
        # "description": p.__doc__.strip(),
    }

with open("resources/permissions.json", "w") as f:
    json.dump(output, f, indent=2)
