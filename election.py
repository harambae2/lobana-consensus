from __future__ import annotations
from typing import Optional, Dict, Iterable, Sequence
from uuid import UUID
from datetime import datetime
from entity import EntitySchema
from ballot import Ballot, CandidateBallotSchema
from poll import Poll
from group import Group, GroupSchema
from candidate import Candidate, CandidateOptionSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Election(Poll):

	__group: Group

	def __init__(self, group: Group, candidates: Iterable[Candidate], ballots: Sequence[Ballot], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(candidates, ballots, identity, timestamp)
		self.__group = group

	def entity(self) -> Group:
		return self.__group

	def __repr__(self) -> str:
		return f'Election(group={pformat(self.entity())}, candidates={pformat(self.options())}, ballots={self.ballots()}, identity={self.identity()}, timestamp={self.timestamp()})'


class ElectionPollSchema(EntitySchema):
	group = fields.Nested(GroupSchema)
	options = fields.List(fields.Nested(CandidateOptionSchema))
	ballots = fields.List(fields.Nested(CandidateBallotSchema))

	@pre_dump
	def serialize_election(self, election: Election, **kwargs) -> Dict:
		return dict(
			group=election.entity(),
			options=election.options(),
			ballots=election.ballots(),
			identity=election.identity(),
			timestamp=election.timestamp()
		)

	@post_load
	def deserialize_election(self, election: Dict, **kwargs) -> Election:
		return Election(
			group=election['group'],
			candidates=election['options'],
			ballots=election['ballots'],
			identity=election['identity'],
			timestamp=election['timestamp']
		)

