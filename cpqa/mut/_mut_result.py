from dataclasses import dataclass
from typing import Any


@dataclass
class MutResult:
    value: Any
    status: str
    is_success: bool

    STATUS_OK = 'OK'

    def __repr__(self):
        return f"MutResult({self.value}, {self.status}, {self.is_success})"
