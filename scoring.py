from __future__ import annotations
from typing import Collection, Tuple, Dict, Iterator
from option import Option
from ranking import Ranking
from itertools import chain

class Scoring(Collection):

	scores: Dict[Option, float]

	def __init__(self: Scoring, scores: Dict[Option, float]) -> None:
		super().__init__()
		self.scores = scores

	def __eq__(self: Scoring, other: object) -> bool:
		if not isinstance(other, Scoring):
			return NotImplemented
		return (super().__eq__(other)) and (self.scores is other.scores)

	def __ne__(self, other: object) -> bool:
		if (result := self is other) is NotImplemented:
			return result
		return not result

	def __len__(self: Scoring) -> int:
		return len(self.scores)

	def __iter__(self: Scoring) -> Iterator[Option]:
		return iter(self.scores)

	def __contains__(self: Scoring, option: object) -> bool:
		if not isinstance(option, Option):
			raise KeyError(option)

		if option in self.scores.values():
			return True
		return False

	def __repr__(self) -> str:
		return f'Scoring(scores={self.scores})'

	def __iadd__(self, other: Scoring) -> Scoring:
		for option, score in other.scores.items():
			self.scores[option] += score
		return self

	def __isub__(self, other: Scoring) -> Scoring:
		for option, score in other.scores.items():
			self.scores[option] -= score
		return self

	@staticmethod
	def score(ranking: Ranking) -> Scoring:
		scores: Dict[Option, float] = {}

		for index, rank in enumerate(reversed(ranking.ranks)):
			if rank:
				for option in rank:
					scores[option] = index + 1

		return Scoring(scores=scores)

	def normalize(self) -> Scoring:
		normalized: Dict[Option, float] = {}
		total: float = sum(score for score in self.scores.values())

		for option, score in self.scores.items():
			normalized[option] = score/total

		return Scoring(scores=normalized)

	def split(self, agreement: Ranking, disagreement: Ranking) -> Tuple[Scoring, Scoring]:
		agreement_scores, disagreement_scores = {}, {}

		for option, score in self.scores.items():
			if option in chain.from_iterable(agreement.ranks):
				agreement_scores[option] = score
			if option in chain.from_iterable(disagreement.ranks):
				disagreement_scores[option] = score

		return (Scoring(scores=agreement_scores), Scoring(scores=disagreement_scores))
