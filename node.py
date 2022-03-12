from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from user import User, UserSchema
from entity import Entity, EntitySchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Node(Entity):

	__user: User
	__trust: float

	def __init__(self, user: User, trust: int, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__user = user
		self.__trust = trust

	def user(self) -> User:
		return self.__user

	def trust(self) -> int:
		return self.__trust

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.user() is other.user()) and (self.trust() is other.trust()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.user(), self.trust(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Node(user={pformat(self.user())}, trust={self.trust()}, identity={self.identity()}, timestamp={self.timestamp()})'

class NodeSchema(EntitySchema):
	user = fields.Nested(UserSchema)
	trust = fields.Float()

	@pre_dump
	def serialize_node(self, node: Node, **kwargs) -> Dict:
		return dict(
			user=node.user(),
			trust=node.trust(),
			identity=node.identity(),
			timestamp=node.timestamp()
		)

	@post_load
	def deserialize_node(self, node: Dict, **kwargs) -> Node:
		return Node(
			user=node['user'],
			trust=node['trust'],
			identity=node['identity'],
			timestamp=node['timestamp']
		)
