from __future__ import annotations
from typing import List, Dict, Optional
from entity import Entity, EntitySchema
from uuid import UUID
from datetime import datetime
from group import Group, GroupSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class User(Entity):

	__groups: List[Group]
	__name: str
	# __admission_id: str
	# __email_id: str
	# __batch: str

	def __init__(self, name: str, groups: List[Group]=[], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__groups = groups
		self.__name = name

	def groups(self, new: Optional[List[Group]]=None) -> List[Group]:
		if new is not None:
			self.__groups = new
		return self.__groups

	def name(self) -> str:
		return self.__name

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.groups() is other.groups()) and (self.name() is other.name()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.name(), super().__hash__()))
	
	def __repr__(self) -> str:
		return f'User(groups={pformat(self.groups())} name={self.name()}, identity={self.identity()}, timestamp={self.timestamp()})'

class UserSchema(EntitySchema):
	groups = fields.List(fields.Nested(GroupSchema))
	name = fields.String()

	@pre_dump
	def serialize_user(self, user: User, **kwargs) -> Dict:
		return dict(
			groups=user.groups(),
			name=user.name(), 
			identity=user.identity(), 
			timestamp=user.timestamp()
		)

	@post_load
	def deserialize_user(self, user: Dict, **kwargs):
		return User(
			groups=user['groups'],
			name=user['name'],
			identity=user['identity'],
			timestamp=user['timestamp']
		)
