from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from entity import EntitySchema
from ballot import Ballot, AnswerBallotSchema
from poll import Poll
from question import Question, QuestionSchema
from answer import Answer, AnswerOptionSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Referendum(Poll):

	__question: Question

	def __init__(self, question: Question, answers: Iterable[Answer], ballots: Sequence[Ballot], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(answers, ballots, identity, timestamp)
		self.__question = question

	def entity(self) -> Question:
		return self.__question

	def __repr__(self) -> str:
		return f'Referendum(question={pformat(self.question())}, answers={pformat(self.options())}, ballots={self.ballots()}, identity={self.identity()}, timestamp={self.timestamp()})'

class ReferendumSchema(EntitySchema):
	question = fields.Nested(QuestionSchema)
	options = fields.List(fields.Nested(AnswerOptionSchema))
	ballots = fields.List(fields.Nested(AnswerBallotSchema))

	@pre_dump
	def serialize_election(self, election: Referendum, **kwargs) -> Dict:
		return dict(
			question=election.entity(),
			options=election.options(),
			ballots=election.ballots(),
			identity=election.identity(),
			timestamp=election.timestamp()
		)

	@post_load
	def deserialize_election(self, election: Dict, **kwargs) -> Referendum:
		return Referendum(
			question=election['question'],
			options=election['options'],
			ballots=election['ballots'],
			identity=election['identity'],
			timestamp=election['timestamp']
		)
