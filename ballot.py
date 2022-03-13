from __future__ import annotations
from typing import Dict, Optional, Tuple
from uuid import UUID
from datetime import datetime
from entity import Entity, EntitySchema
from ranking import Ranking, CandidateRankingSchema, AnswerRankingSchema
from scoring import Scoring
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Ballot(Entity):

	__agreement: Ranking
	__disagreement: Ranking

	def __init__(self, agreement: Ranking=Ranking(), disagreement: Ranking=Ranking(), identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__agreement = agreement
		self.__disagreement = disagreement

	def agreement(self) -> Ranking:
		return self.__agreement

	def disagreement(self) -> Ranking:
		return self.__disagreement

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Ballot):
			return NotImplemented
		return (self.agreement() is other.agreement()) and (self.disagreement() is other.disagreement()) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.agreement(), self.disagreement(), super().__hash__()))
		
	def __repr__(self) -> str:
		return f'Ballot(agreement={pformat(self.agreement())}, disagreement={pformat(self.disagreement())}, identity={self.identity()}, timestamp={self.timestamp()})'

	def normalize(self) -> Tuple[Scoring, Scoring]:
		merged_ranking: Ranking = Ranking.merge(self.agreement(), self.disagreement())
		merged_scoring: Scoring = Scoring.score(merged_ranking)
		normalized_scoring: Scoring = merged_scoring.normalize()
		return normalized_scoring.split(self.agreement(), self.disagreement())

class CandidateBallotSchema(EntitySchema):
	agreement = fields.Nested(CandidateRankingSchema)
	disagreement = fields.Nested(CandidateRankingSchema)

	@pre_dump
	def serialize_ballot(self, ballot: Ballot, **kwargs) -> Dict:
		return dict(
			agreement=ballot.agreement(),
			disagreement=ballot.disagreement(),
			identity=ballot.identity(),
			timestamp=ballot.timestamp()
		)

	@post_load
	def deserialize_ballot(self, ballot: Dict, **kwargs) -> Ballot:
		return Ballot(
			agreement=ballot['agreement'],
			disagreement=ballot['disagreement'],
			identity=ballot['identity'],
			timestamp=ballot['timestamp']
		)

class AnswerBallotSchema(EntitySchema):
	agreement = fields.Nested(AnswerRankingSchema)
	disagreement = fields.Nested(AnswerRankingSchema)

	@pre_dump
	def serialize_ballot(self, ballot: Ballot, **kwargs) -> Dict:
		return dict(
			agreement=ballot.agreement(),
			disagreement=ballot.disagreement(),
			identity=ballot.identity(),
			timestamp=ballot.timestamp()
		)

	@post_load
	def deserialize_ballot(self, ballot: Dict, **kwargs) -> Ballot:
		return Ballot(
			agreement=ballot['agreement'],
			disagreement=ballot['disagreement'],
			identity=ballot['identity'],
			timestamp=ballot['timestamp']
		)
