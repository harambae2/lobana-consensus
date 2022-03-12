from __future__ import annotations
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from entity import Entity, EntitySchema
from option import Option
from candidate import CandidateOptionSchema
from answer import AnswerOptionSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Ranking(Entity):

	__ranks: List[List[Option]]

	def __init__(self, ranks: List[List[Option]]=[], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__ranks = ranks

	def ranks(self) -> List[List[Option]]:
		return self.__ranks

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.ranks() is other.ranks()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.ranks(), super().__hash__()))

	def __len__(self) -> int:
		return len(self.ranks())

	def __repr__(self) -> str:
		return f'Ranking(ranks={pformat(self.ranks())}, identity={self.identity()}, timestamp={self.timestamp()})'

	@staticmethod
	def merge(this: Ranking, that: Ranking) -> Ranking:

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

class CandidateRankingSchema(EntitySchema):
	ranks = fields.List(fields.List(fields.Nested(CandidateOptionSchema)))

	@pre_dump
	def serialize_ranking(self, ranking: Ranking, **kwargs) -> Dict:
		return dict(
			ranks=ranking.ranks(),
			identity=ranking.identity(),
			timestamp=ranking.timestamp()
		)

	@post_load
	def deserialize_ranking(self, ranking: Dict, **kwargs) -> Ranking:
		return Ranking(
			ranks=ranking['ranks'],
			identity=ranking['identity'],
			timestamp=ranking['timestamp']
		)

class AnswerRankingSchema(EntitySchema):
	ranks = fields.List(fields.List(fields.Nested(AnswerOptionSchema)))

	@pre_dump
	def serialize_ranking(self, ranking: Ranking, **kwargs) -> Dict:
		return dict(
			ranks=ranking.ranks(),
			identity=ranking.identity(),
			timestamp=ranking.timestamp()
		)

	@post_load
	def deserialize_ranking(self, ranking: Dict, **kwargs) -> Ranking:
		return Ranking(
			ranks=ranking['ranks'],
			identity=ranking['identity'],
			timestamp=ranking['timestamp']
		)
