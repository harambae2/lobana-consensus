from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from option import Option
from entity import EntitySchema
from user import User, UserSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Candidate(Option):

	__user: User

	def __init__(self, user: User, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__user = user

	def entity(self) -> User:
		return self.__user
	
	def __repr__(self) -> str:
		return f'Candidate(user={pformat(self.entity())}, identity={self.identity()}, timestamp={self.timestamp()})'

class CandidateOptionSchema(EntitySchema):
	user = fields.Nested(UserSchema)

	@pre_dump
	def serialize_option(self, candidate: Candidate, **kwargs) -> Dict:
		return dict(
			user=candidate.entity(),
			identity=candidate.identity(),
			timestamp=candidate.timestamp()
		)

	@post_load
	def deserialize_option(self, candidate: Dict, **kwargs) -> Candidate:
		return Candidate(
			user=candidate['user'],
			identity=candidate['identity'],
			timestamp=candidate['timestamp']
		)
