from __future__ import annotations
from typing import Iterable, List, Optional, Sequence
from collections import OrderedDict
from abc import ABC, abstractmethod, abstractproperty
from uuid import UUID
from datetime import datetime
from entity import Entity
from ballot import Ballot
from option import Option
from scoring import Scoring

class Poll(Entity, ABC):

	__options: Iterable[Option]
	__ballots: Sequence[Ballot]

	def __init__(self, options: Iterable[Option], ballots: Sequence[Ballot], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__options = options
		self.__ballots = ballots

	def options(self) -> Iterable[Option]:
		return self.__options

	def ballots(self, new: Optional[Sequence[Ballot]]=None) -> Sequence[Ballot]:
		if new is not None:
			self.__ballots = new
		return self.__ballots
	
	@abstractproperty
	def entity(self) -> Entity:
		pass

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Poll):
			return NotImplemented
		return (self.entity is other.entity) and (self.options() is other.options()) and (self.ballots() is other.ballots()) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result
			
	def __hash__(self) -> int:
		return hash((self.entity, self.options(), self.ballots(), super().__hash__()))

	@abstractmethod
	def __repr__(self) -> str:
		pass

	def count(self) -> Scoring:
		scores: Scoring = Scoring({option : 0 for option in self.options()})
		
		for ballot in self.ballots():
			agreement_scores, disagreement_scores = ballot.normalize()
			scores += agreement_scores
			scores -= disagreement_scores

		return scores

	def consensus(self) -> Scoring:
		probability: float = 0
		selected: Scoring = Scoring({})
		scores: OrderedDict = OrderedDict(self.count().scores())

		for option in reversed(scores):
			if probability <= 1:
				if (average := scores[option] / len(self.ballots())) > 0:
					selected.scores({option: average, **selected.scores()})
					probability += average
			else:
				break
		
		return selected
