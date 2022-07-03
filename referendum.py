from __future__ import annotations
from typing import Optional, Iterable, Sequence
from group import Group
from option import Option
from poll import Poll
from question import Question
from answer import Answer

class Referendum(Poll):

	__question: Question

	def __init__(self: Referendum, voters: Iterable[Group], answers: Iterable[Answer], question: Question) -> None:
		super().__init__(voters, answers)
		self.__question = question

	@property
	def question(self: Referendum) -> Question:
		return self.__question

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Poll):
			return NotImplemented
		return (self.question is other.question) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		return not result

	def __hash__(self) -> int:
		return hash((super().__hash__(), self.question))

	def __repr__(self) -> str:
		return f'Referendum(entity={super().__repr__()}, question={self.question}, answers={self.options}, ballots={self.ballots})'
