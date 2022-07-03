from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime

class Entity(object):

	__identity: UUID = uuid4()
	__timestamp: datetime = datetime.now()

	def __init__(self: Entity) -> None:
		self.__identity = uuid4()
		self.__timestamp = datetime.now()

	@property
	def identity(self: Entity) -> UUID:
		return self.__identity

	@property
	def timestamp(self: Entity) -> datetime:
		return self.__timestamp
	
	def __eq__(self: Entity, other: object) -> bool:
		if not isinstance(other, Entity):
			return NotImplemented
		return (self.identity is other.identity) and (self.timestamp is other.timestamp)

	def __ne__(self: Entity, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __hash__(self: Entity) -> int:
		return hash((super().__hash__(), self.identity, self.timestamp))

	def __repr__(self: Entity) -> str:
		return f"Entity(identity={repr(self.identity)}, timestamp={repr(self.timestamp)})"
