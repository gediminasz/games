from dataclasses import dataclass

from .store import Store


@dataclass
class Scene:
    store: Store
