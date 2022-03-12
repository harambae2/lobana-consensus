from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from entity import Entity, EntitySchema
from pprint import pformat
from marshmallow import fields, pre_dump, post_load

class Question(Entity):

	__text: str

	def __init__(self, text: str='', identity: Optional[UUID]=None, timestamp: Optional[datetime]=None) -> None:
		super().__init__(identity, timestamp)
		self._text = text

	def text(self) -> str:
		return self.__text

	def __eq__(self, other: object) -> bool:
		if self.__class__ is other.__class__:
			return (self.text() is other.text()) and (super() is other)
		else:
			return NotImplemented

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return NotImplemented
		else:
			return not result

	def __hash__(self) -> int:
		return hash((self.text(), super().__hash__()))

	def __repr__(self) -> str:
		return f'Question(text={pformat(self.text())}, identity={self.identity()}, timestamp={self.timestamp()})'

class QuestionSchema(EntitySchema):
	text = fields.String()

	@pre_dump
	def serialize_option(self, question: Question, **kwargs) -> Dict:
		return dict(
			text=question.text(),
			identity=question.identity(),
			timestamp=question.timestamp()
		)

	@post_load
	def deserialize_option(self, question: Dict, **kwargs) -> Question:
		return Question(
			text=question['text'],
			identity=question['identity'],
			timestamp=question['timestamp']
		)
