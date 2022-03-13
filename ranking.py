from __future__ import annotations
import imp
from re import L
from typing import List, Dict
from option import Option
from candidate import CandidateOptionSchema
from answer import AnswerOptionSchema
from pprint import pformat
from marshmallow import Schema, fields, pre_dump, post_load

class Ranking:

	__ranks: List[List[Option]]

	def __init__(self, ranks: List[List[Option]]=[]) -> None:
		self.__ranks = ranks

	def ranks(self) -> List[List[Option]]:
		return self.__ranks

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Ranking):
			return NotImplemented
		return self.ranks() is other.ranks()

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash(self.ranks())

	def __len__(self) -> int:
		return len(self.ranks())

	def __repr__(self) -> str:
		return f'Ranking(ranks={pformat(self.ranks())})'

	@staticmethod
	def merge(this: Ranking, that: Ranking) -> Ranking:

		merged: List[List[Option]] = []

		if len(this) > len(that):
			merged = [[] for _ in this.ranks()]
		else:
			merged = [[] for _ in that.ranks()]

		for index, rank in enumerate(this.ranks()):
			if rank:
				merged[index].extend(rank)

		for index, rank in enumerate(that.ranks()):
			if rank:
				merged[index].extend(rank)

		return Ranking(merged)

class RankingSchema(Schema):
	@pre_dump
	def serialize_ranking(self, ranking: Ranking, **kwargs) -> Dict:
		return dict(
			ranks=ranking.ranks(),
		)

	@post_load
	def deserialize_ranking(self, ranking: Dict, **kwargs) -> Ranking:
		return Ranking(
			ranks=ranking['ranks'],
		)

class CandidateRankingSchema(RankingSchema):
	ranks = fields.List(fields.List(fields.Nested(CandidateOptionSchema)))


class AnswerRankingSchema(RankingSchema):
	ranks = fields.List(fields.List(fields.Nested(AnswerOptionSchema)))
