from __future__ import annotations
from typing import List, Optional
from abc import ABC, abstractmethod, abstractproperty
from uuid import UUID
from datetime import datetime
from entity import Entity
from ballot import Ballot
from option import Option
from scoring import Scoring

class Poll(Entity, ABC):

	__options: List[Option]
	__ballots: List[Ballot]

	def __init__(self, options: List[Option], ballots: List[Ballot], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__options = options
		self.__ballots = ballots

	def options(self) -> List[Option]:
		return self.__options

	def ballots(self) -> List[Ballot]:
		return self.__ballots
	
	@abstractproperty
	def entity(self) -> Entity:
		pass

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.entity() is other.entity()) and (self.options() is other.options()) and (self.ballots() is other.ballots()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result
			
	def __hash__(self) -> int:
		return hash((self.entity(), self.options(), self.ballots(), super().__hash__()))

	@abstractmethod
	def __repr__(self) -> str:
		pass

	def count(self) -> Scoring:
		scores = Scoring({option : 0 for option in self.options()})
		
		for ballot in self.ballots():
			agreement_scores, disagreement_scores = ballot.normalize()
			scores += agreement_scores
			scores -= disagreement_scores

		return scores

	def consensus(self) -> List[Option]:
		probability = 0
		selected = []
		count = self.count()
		scores = count.scores()

		for option in sorted(scores, key=scores.get, reverse=True):
			if probability <= 1:
				if (average := scores[option] / len(self.ballots())) > 0:
					selected.append(option)
					probability += average
			else:
				break
		
		return selected
