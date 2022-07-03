from __future__ import annotations
from abc import ABC, abstractmethod
from entity import Entity

class Option(Entity, ABC):

	@abstractmethod
	def __init__(self: Option) -> None:
		pass

	@abstractmethod
	def __eq__(self: Option, other: object) -> bool:
		if not isinstance(other, Option):
			return NotImplemented
		return super().__eq__(other)
	
	@abstractmethod
	def __ne__(self: Option, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	@abstractmethod
	def __hash__(self: Option) -> int:
		return super().__hash__()

	@abstractmethod
	def __repr__(self) -> str:
		pass
