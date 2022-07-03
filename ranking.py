from __future__ import annotations
from typing import Collection, List, Optional, Iterator
from option import Option

class Ranking(Collection):

	ranks: List[List[Option]]

	def __init__(self: Ranking, ranks: Optional[ranks]=[]):
		self.ranks = ranks

	def __eq__(self: Ranking, other: object) -> bool:
		if not isinstance(other, Ranking):
			return NotImplemented
		return (super().__eq__(other)) and (self.ranks is other.ranks)

	def __ne__(self: Ranking, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __len__(self: Ranking) -> int:
		return len(self.ranks)

	def __iter__(self) -> Iterator[List[Option]]:
		return iter(self.ranks)
	
	def __contains__(self, option: object) -> bool:
		if not isinstance(option, Option):
			raise KeyError(option)

		for rank in self.ranks:
			if option in rank:
				return True
		return False
	
	def __repr__(self) -> str:
		return f'Ranking(ranks={repr(self.ranks)})'

	@staticmethod
	def merge(this: Ranking, that: Ranking) -> Ranking:

		merged: List[List[Option]] = []

		if len(this) > len(that):
			merged = [[] for _ in this.ranks]
		else:
			merged = [[] for _ in that.ranks]

		for index, rank in enumerate(this.ranks):
			if rank:
				merged[index].extend(rank)

		for index, rank in enumerate(that.ranks):
			if rank:
				merged[index].extend(rank)

		return Ranking(ranks=merged)
