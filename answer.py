from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from option import Option
from entity import EntitySchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Answer(Option):

	__text: str

	def __init__(self, text: str, identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self.__text = text

	def entity(self) -> str:
		return self.__text

	def __repr__(self) -> str:
		return f'Answer(text={pformat(self.entity())}, identity={self.identity()}, timestamp={self.timestamp()})'

class AnswerOptionSchema(EntitySchema):
	text = fields.String()

	@pre_dump
	def serialize_option(self, answer: Answer, **kwargs) -> Dict:
		return dict(
			text=answer.entity(),
			identity=answer.identity(),
			timestamp=answer.timestamp()
		)

	@post_load
	def deserialize_option(self, answer: Dict, **kwargs) -> Answer:
		return Answer(
			text=answer['text'],
			identity=answer['identity'],
			timestamp=answer['timestamp']
		)
