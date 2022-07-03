from __future__ import annotations
from entity import Entity

class Question(Entity):

	__text: str

	def __init__(self, text: str) -> None:
		super().__init__()
		self.__text = text

	@property
	def text(self) -> str:
		return self.__text

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Question):
			return NotImplemented
		return (super().__eq__(other)) and (self.text is other.text)

	def __ne__(self: Question, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		return not result

	def __hash__(self: Question) -> int:
		return hash((super().__hash__(), self.text))

	def __repr__(self: Question) -> str:
		return f'Question(entity={super().__repr__()}, text={repr(self.text)})'
