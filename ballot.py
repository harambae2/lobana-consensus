from __future__ import annotations
from typing import Optional, Tuple
from entity import Entity
from ranking import Ranking
from scoring import Scoring

class Ballot(Entity):

	agreement: Ranking
	disagreement: Ranking

	def __init__(self: Entity, agreement: Ranking, disagreement: Ranking) -> None:
		super().__init__()
		self.agreement = agreement
		self.disagreement = disagreement

	def __eq__(self: Ballot, other: object) -> bool:
		if not isinstance(other, Ballot):
			return NotImplemented
		return (super().__eq__(other)) and (self.agreement is other.agreement) and (self.disagreement is other.disagreement)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result
		
	def __repr__(self) -> str:
		return f'Ballot(entity={super().__repr__()}, agreement={repr(self.agreement)}, disagreement={repr(self.disagreement)})'

	def normalize(self) -> Tuple[Scoring, Scoring]:
		merged_ranking: Ranking = Ranking.merge(self.agreement, self.disagreement)
		merged_scoring: Scoring = Scoring.score(merged_ranking)
		normalized_scoring: Scoring = merged_scoring.normalize()
		return normalized_scoring.split(self.agreement, self.disagreement)
