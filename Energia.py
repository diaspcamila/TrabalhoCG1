from enum import Enum, auto
from dataclasses import dataclass

class EnergiaStatus(Enum):
    VIVO = auto()
    MORTO = auto()
    REPRODUZINDO = auto()

@dataclass
class StatusEnergia:
    status: EnergiaStatus
