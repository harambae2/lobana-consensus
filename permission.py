from __future__ import annotations
from datetime import datetime
from typing import Optional, Dict
from entity import Entity, EntitySchema
from uuid import UUID
from marshmallow import fields, pre_dump, post_load

class Permission(Entity):

	__read: bool
	__write: bool
	__execute: bool

	def __init__(self, read: bool, write: bool, execute: bool, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__read = read
		self.__write = write
		self.__execute = execute

	def read(self) -> bool:
		return self.__read

	def write(self) -> bool:
		return self.__write

	def execute(self) -> bool:
		return self.__execute

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Permission):
			return NotImplemented
		return (self.read() is other.read()) and (self.write() is other.write()) and (self.execute() is other.execute()) and (super() is other)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.read(), self.write(), self.execute(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Permission(read={self.read()}, write={self.write()}, execute={self.execute()}, identity={self.identity()}, timestamp={self.timestamp()})'

class PermissionSchema(EntitySchema):
	read = fields.Boolean()
	write = fields.Boolean()
	execute = fields.Boolean()

	@pre_dump
	def serialize_permission(self, permission: Permission, **kwargs) -> Dict:
		return dict(
			read=permission.read(),
			write=permission.write(),
			execute=permission.execute(),
			identity=permission.identity(),
			timestamp=permission.timestamp()
		)

	@post_load
	def deserialize_permission(self, permission: Dict, **kwargs) -> Permission:
		return Permission(
			read=permission['read'],
			write=permission['write'],
			execute=permission['execute'],
			identity=permission['identity'],
			timestamp=permission['timestamp']
		)


# class Votable(Permission(read=True, write=True, execute=True)):
# 	pass

# class NotVotable(Permission(read=True, write=False, execute=False)):
# 	pass

# class Answerable(Permission(read=True, write=True, execute=True)):
# 	pass

# class NotAnswerable(Permission(read=True, write=False, execute=False)):
# 	pass
