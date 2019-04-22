from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AttackType(Enum):
    STAB = "stab"
    MAGIC = "magic"
    DEFENSIVE_CASTING = "defensive casting"
    SLASH = "slash"
    RANGED = "ranged"
    SPELLCASTING = "spellcasting"
    CRUSH = "crush"
    NONE = None
    ALIAS_FOR_NONE = "none"


class AttackStyle(Enum):
    ACCURATE = "accurate"
    AGGRESSIVE = "aggressive"
    MAGIC = "magic"
    DEFENSIVE = "defensive"
    CONTROLLED = "controlled"
    NONE = None
    ALIAS_FOR_NONE = "none"


@dataclass
class Stance:
    boosts: Optional[str]
    combat_style: str
    experience: str

    attack_type: AttackType
    attack_style: AttackStyle

    @classmethod
    def from_json(cls, json_dict):
        return cls(
            attack_type=AttackType(json_dict.pop("attack_type")),
            attack_style=AttackStyle(json_dict.pop("attack_style")),
            **json_dict
        )
