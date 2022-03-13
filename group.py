from __future__ import annotations
from typing import Iterable, Optional, Dict
from entity import Entity, EntitySchema
from permission import Permission, PermissionSchema
from uuid import UUID
from datetime import datetime
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Group(Entity):

	_name: str
	__permissions: Iterable[Permission]

	def __init__(self, name: str, permissions: Iterable[Permission], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__name = name
		self.__permissions = permissions

	def name(self) -> str:
		return self.__name

	def permissions(self, new: Optional[Iterable[Permission]]=None) -> Iterable[Permission]:
		if new is not None:
			self.__permissions = new
		return self.__permissions		

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Group):
			return NotImplemented
		return (self.name() is other.name()) and (self.permissions() is other.permissions()) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.name(), self.permissions(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Group(name={self.name()}, permissions={pformat(self.permissions())}, identity={self.identity()}, timestamp={self.timestamp()})'

class GroupSchema(EntitySchema):
	permissions = fields.List(fields.Nested(PermissionSchema))

	@pre_dump
	def serialize_group(self, group: Group, **kwargs) -> Dict:
		return dict(
			name=group.name(),
			permissions=group.permissions(),
			identity=group.identity(),
			timestamp=group.timestamp()
		)

	@post_load
	def deserialize_group(self, group: Dict, **kwargs) -> Group:
		return Group(
			name=group['name'],
			permissions=group['permissions'],
			identity=group['identity'],
			timestamp=group['timestamp']
		)


# class Electorate(Group(permissions=Voting)):
	
# 	def __init__(self, uuid: UUID=None, users: List[User]=None) -> None:
# 		super().__init__(uuid=uuid, users=users)
	
# class Slate(Electorate):
	
# 	def __init__(self, uuid: UUID=None, users: List[User]=None) -> None:
# 		super().__init__(uuid=uuid, users=users)

# class Independent(Slate):

# 	def __init__(self, uuid: UUID=None, users: List[User]=None) -> None:
# 		super().__init__(uuid=uuid, users=users)

# class Party(Group(permissions=NonVoting)):

# 	def __init__(self, uuid: UUID=None, users: List[User]=None) -> None:
# 		super().__init__(uuid=uuid, users=users)