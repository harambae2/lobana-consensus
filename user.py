from __future__ import annotations
from typing import Iterable, Dict, Optional
from entity import Entity, EntitySchema
from uuid import UUID
from datetime import datetime
from group import Group, GroupSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class User(Entity):

	__name: str
	__groups: Iterable[Group]

	def __init__(self, name: str, groups: Iterable[Group], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__name = name
		self.__groups = groups
	
	def name(self) -> str:
		return self.__name

	def groups(self, new: Optional[Iterable[Group]]=None) -> Iterable[Group]:
		if new is not None:
			self.__groups = new
		return self.__groups

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, User):
			return NotImplemented
		return (self.name() is other.name()) and (self.groups() is other.groups()) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.name(), super().__hash__()))
	
	def __repr__(self) -> str:
		return f'User(name={self.name()}, groups={pformat(self.groups())}, identity={self.identity()}, timestamp={self.timestamp()})'

class UserSchema(EntitySchema):
	name = fields.String()
	groups = fields.List(fields.Nested(GroupSchema))

	@pre_dump
	def serialize_user(self, user: User, **kwargs) -> Dict:
		return dict(
			name=user.name(), 
			groups=user.groups(),
			identity=user.identity(), 
			timestamp=user.timestamp()
		)

	@post_load
	def deserialize_user(self, user: Dict, **kwargs):
		return User(
			name=user['name'],
			groups=user['groups'],
			identity=user['identity'],
			timestamp=user['timestamp']
		)
