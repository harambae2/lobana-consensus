from __future__ import annotations
from typing import Iterable, Sequence
from abc import ABC, abstractmethod
from entity import Entity
from group import Group
from option import Option
from ballot import Ballot
from scoring import Scoring
from collections import OrderedDict

class Poll(Entity, ABC):

	__voters: Iterable[Group]
	__options: Iterable[Option]
	ballots: Sequence[Ballot]

	def __init__(self: Poll, voters: Iterable[Group], options: Iterable[Option]) -> None:
		super().__init__()
		self.__voters = voters
		self.__options = options
		self.ballots = []

	@property
	def voters(self: Poll) -> Iterable[Group]:
		return self.__voters

	@property
	def options(self: Poll) -> Iterable[Option]:
		return self.__options

	@abstractmethod
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Poll):
			return NotImplemented
		return (super().__eq__(other)) and (self.voters is other.voters) and (self.options is other.options) and (self.ballots is other.ballots)

	@abstractmethod
	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	@abstractmethod
	def __hash__(self: Poll) -> int:
		return hash((super().__hash__()))

	@abstractmethod
	def __repr__(self) -> str:
		pass

	def count(self) -> Scoring:
		scores: Scoring = Scoring(scores={option : 0 for option in self.options})
		
		for ballot in self.ballots:
			agreement_scores, disagreement_scores = ballot.normalize()
			scores += agreement_scores
			scores -= disagreement_scores

		return scores

	def consensus(self) -> Scoring:
		probability: float = 0
		selected: Scoring = Scoring(scores={})
		scores: OrderedDict = OrderedDict(self.count().scores)

		for option in reversed(scores):
			if probability <= 1:
				if (average := scores[option] / len(self.ballots)) > 0:
					selected.scores[option] = average
					probability += average
			else:
				break
		
		return selected
