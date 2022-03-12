from __future__ import annotations
from typing import Tuple, Dict, Optional
from uuid import UUID
from datetime import datetime
from entity import Entity, EntitySchema
from option import Option
from candidate import CandidateOptionSchema
from answer import AnswerOptionSchema
from ranking import Ranking
from itertools import chain
from pprint import pformat
from marshmallow import Schema, fields, pre_dump, post_load

class Scoring(Entity):

	__scores: Dict[Option, float]

	def __init__(self, scores: Dict[Option, float], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__scores = scores

	def scores(self) -> Dict[Option, float]:
		return self.__scores

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.scores is other.scores) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.scores(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Scoring(scores={pformat(self.scores())}, identity={self.identity()}, timestamp={self.timestamp()})'

	# def __add__(self, other: Scoring) -> Scoring:
	# 	for option, score in other.scores().items():
	# 		self.__scores[option] += score
	# 	return self

	# def __sub__(self, other: Scoring) -> Scoring:
	# 	for option, score in other.scores().items():
	# 		self.__scores[option] -= score
	# 	return self

	def __iadd__(self, other: Scoring) -> Scoring:
		for option, score in other.scores().items():
			self.__scores[option] += score
		return self

	def __isub__(self, other: Scoring) -> Scoring:
		for option, score in other.scores().items():
			self.__scores[option] -= score
		return self

	@staticmethod
	def score(ranking: Ranking) -> Scoring:
		scores: Dict[Option, float] = {}

		for index, rank in enumerate(reversed(ranking.ranks())):
			if rank:
				for option in rank:
					scores[option] = index + 1

		return Scoring(scores)

	def normalize(self) -> Scoring:
		normalized: Dict[Option, float] = {}
		total = sum(score for score in self.scores().values())

		for option, score in self.scores().items():
			normalized[option] = score/total

		return Scoring(normalized)

	def split(self, agreement: Ranking, disagreement: Ranking) -> Tuple[Scoring, Scoring]:
		agreement_scores, disagreement_scores = {}, {}

		for option, score in self.scores().items():
			if option in chain.from_iterable(agreement.ranks()):
				agreement_scores[option] = score
			if option in chain.from_iterable(disagreement.ranks()):
				disagreement_scores[option] = score

		return (Scoring(agreement_scores), Scoring(disagreement_scores))

class ScoreSchema(Schema):
	score = fields.Float()

	@pre_dump
	def serialize_score(self, score: Tuple[Option, float], **kwargs) -> Dict:
		return dict(option=score[0], score=score[1])

	@post_load
	def deserialize_score(self, score: Dict, **kwargs) -> Tuple[Option, float]:
		return (score['option'], score['score'])

class CandidateScoreSchema(ScoreSchema):
	option = fields.Nested(CandidateOptionSchema)

class AnswerScoreSchema(ScoreSchema):
	option = fields.Nested(AnswerOptionSchema)

class ScoringSchema(EntitySchema):

	@pre_dump
	def serialize_scoring(self, scoring: Scoring, **kwargs) -> Dict:
		return dict(
			scores=[(option, score) for option, score in scoring.scores().items()],
			identity=scoring.identity(),
			timestamp=scoring.timestamp()
		)

	@post_load
	def deserialize_scoring(self, scoring: Dict, **kwargs) -> Scoring:
		return Scoring(
			scores={option: score for option, score in scoring['scores']},
			identity=scoring['identity'],
			timestamp=scoring['timestamp']
		)

class CandidateScoringSchema(ScoringSchema):
	scores = fields.List(fields.Nested(CandidateScoreSchema))

class AnswerScoringSchema(ScoringSchema):
	scores = fields.List(fields.Nested(AnswerScoreSchema))

