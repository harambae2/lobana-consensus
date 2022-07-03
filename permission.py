from __future__ import annotations
from entity import Entity

class Permission(Entity):

	__read: bool
	__write: bool
	__execute: bool

	def __init__(self: Permission, read: bool, write: bool, execute: bool) -> None:
		super().__init__()
		self.__read = read
		self.__write = write
		self.__execute = execute

	@property
	def read(self: Permission) -> bool:
		return self.__read

	@property
	def write(self: Permission) -> bool:
		return self.__write

	@property
	def execute(self: Permission) -> bool:
		return self.__execute

	def __eq__(self: Entity, other: object) -> bool:
		if not isinstance(other, Entity):
			return NotImplemented
		return (super().__eq__(other)) and (self.read is other.read) and (self.write is other.write) and (self.execute is other.execute)

	def __ne__(self: Entity, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __hash__(self: Entity) -> int:
		return hash((super().__hash__(), self.read, self.write, self.execute))

	def __repr__(self: Entity) -> str:
		return f"Permission(entity={super().__repr__()}, read={repr(self.read)}, write={repr(self.write)}, execute={repr(self.execute)})"
