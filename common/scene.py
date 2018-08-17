from dataclasses import dataclass

from .store import Store


@dataclass(frozen=True)
class Scene:
    store: Store
