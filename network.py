from __future__ import annotations
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime
from entity import Entity, EntitySchema
from node import Node, NodeSchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Network(Entity):

	__nodes: List[Node]

	def __init__(self, nodes: List[Node], identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__nodes = nodes
	
	def nodes(self) -> List[Node]:
		return self.__nodes

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.nodes() is other.nodes()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.nodes(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Network(nodes={pformat(self.nodes())}, identity={self.identity()}, timestamp={self.timestamp()})'

class NetworkSchema(EntitySchema):
	nodes = fields.List(fields.Nested(NodeSchema))

	@pre_dump
	def serialize_network(self, network: Network, **kwargs) -> Dict:
		return dict(
			nodes=network.nodes(),
			identity=network.identity(),
			timestamp=network.timestamp()
		)

	@post_load
	def deserialize_network(self, network: Dict, **kwargs) -> Network:
		return Network(
			nodes=network['nodes'],
			identity=network['identity'],
			timestamp=network['timestamp']
		)
