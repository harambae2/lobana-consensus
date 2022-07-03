from __future__ import annotations
from option import Option

class Answer(Option):

	__text: str

	def __init__(self: Answer, text: str) -> None:
		super().__init__()
		self.__text = text

	@property
	def text(self: Answer) -> str:
		return self.__text

	def __eq__(self: Answer, other: object) -> bool:
		if not isinstance(other, Answer):
			return NotImplemented
		return (super().__eq__(other)) and (self.text is other.text)
	
	def __ne__(self: Answer, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __hash__(self: Answer) -> int:
		return hash((super().__hash__(), self.text))

	def __repr__(self: Answer) -> str:
		return f'Answer(text={repr(self.text)})'
