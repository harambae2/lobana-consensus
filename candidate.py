from __future__ import annotations
from option import Option
from user import User

class Candidate(Option):

	__user: User

	def __init__(self: Candidate, user: User) -> None:
		self.__user = user

	@property
	def user(self: Candidate) -> User:
		return self.__user

	def __eq__(self: Candidate, other: object) -> bool:
		if not isinstance(other, Candidate):
			return NotImplemented
		return (super().__eq__(other)) and (self.user is other.user)
	
	def __ne__(self: Candidate, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __hash__(self: Candidate) -> int:
		return hash((super().__hash__(), self.user))
	
	def __repr__(self: Candidate) -> str:
		return f'Candidate(user={repr(self.user)})'
