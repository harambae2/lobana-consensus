from __future__ import annotations
from typing import Iterable
from entity import Entity
from permission import Permission

class Group(Entity):

	name: str 
	permissions: Iterable[Permission]

	def __init__(self: Group, name: str, permissions: Iterable[Permission]) -> None:
		super().__init__()
		self.name = name
		self.permissions = permissions

	def __eq__(self: Group, other: object) -> bool:
		if not isinstance(other, Group):
			return NotImplemented
		return (super().__eq__(other)) and (self.name is other.name) and (self.permissions is other.permissions)

	def __ne__(self: Group, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result
	
	def __hash__(self: Entity) -> int:
		return hash((super().__hash__(), self.name))

	def __repr__(self: Group) -> str:
		return f"Group(entity={super().__repr__()}, name={repr(self.name)}, permissions={repr(self.permissions)})"
