from __future__ import annotations
from typing import Iterable
from poll import Poll
from user import User
from group import Group
from candidate import Candidate

class Election(Poll):

	__group: Group

	def __init__(self: Election, group: Group, voters: Iterable[User], candidates: Iterable[Candidate]) -> None:
		super().__init__(voters, candidates)
		self.__group = group
	
	@property
	def group(self: Election) -> Group:
		return self.__group

	def __eq__(self: Election, other: object) -> bool:
		if not isinstance(other, Election):
			return NotImplemented
		return (self.group is other.group) and (super() is other)

	def __ne__(self: Election, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		return not result

	def __hash__(self: Election) -> int:
		return hash((super().__hash__(), self.group))

	def __repr__(self: Election) -> str:
		return f'Election(entity={super().__repr__()}, group={repr(self.group)}, candidates={repr(self.options)}, ballots={repr(self.ballots)})'
