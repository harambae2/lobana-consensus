from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from marshmallow import Schema, fields

class Entity(ABC):

	__identity: UUID
	__timestamp: datetime

	def __init__(self, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__()
		self.__identity = uuid4() if identity is None else identity
		self.__timestamp = datetime.now() if timestamp is None else timestamp

	def identity(self):
		return self.__identity

	def timestamp(self):
		return self.__timestamp

	@abstractmethod
	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.identity() is other.identity()) and (self.timestamp() is other.timestamp()) and (super() is other)
		else:
			return NotImplemented

	@abstractmethod
	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	@abstractmethod
	def __hash__(self) -> int:
		return hash((self.identity(), self.timestamp(), super().__hash__()))

	@abstractmethod
	def __repr__(self) -> str:
		pass

class EntitySchema(Schema):
	identity = fields.UUID()
	timestamp = fields.DateTime()
