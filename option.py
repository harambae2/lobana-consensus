from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod, abstractproperty
from uuid import UUID
from datetime import datetime
from entity import Entity
from pprint import pformat

class Option(Entity, ABC):

	def __init__(self, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)

	@abstractproperty
	def entity(self) -> Entity:
		pass

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.entity() is other.entity()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.entity(), super().__hash__()))

	@abstractmethod
	def __repr__(self) -> str:
		pass
