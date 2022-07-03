from __future__ import annotations
from typing import Iterable
from entity import Entity
from group import Group

class User(Entity):

	name: str
	groups: Iterable[Group]

	def __init__(self: User, name: str, groups: Iterable[Group]) -> None:
		super().__init__()
		self.name = name
		self.groups = groups
	
	def __eq__(self: User, other: object) -> bool:
		if not isinstance(other, User):
			return NotImplemented
		return (super().__eq__(other)) and (self.name is other.name) and (self.groups is other.groups)

	def __ne__(self: User, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __hash__(self: User) -> int:
		return hash((super().__hash__(), self.name))
	
	def __repr__(self: User) -> str:
		return f"User(entity={super().__repr__()}, name={repr(self.name)}, groups={repr(self.groups)})"
