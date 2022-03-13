from __future__ import annotations
from permission import Permission
from group import Group
from user import User
from candidate import Candidate, CandidateOptionSchema
from ballot import Ballot
from ranking import Ranking
from group import Group
from election import Election, ElectionPollSchema
from scoring import CandidateScoringSchema

if __name__ == '__main__':

	g = Group('Group 0', [Permission(read=False, write=False, execute=False)])

	u0 = User('User 0', [g])
	u1 = User('User 1', [g])
	u2 = User('User 2', [g])
	u3 = User('User 3', [g])
	u4 = User('User 4', [g])
	u5 = User('User 5', [g])
	u6 = User('User 6', [g])
	u7 = User('User 7', [g])
	u8 = User('User 8', [g])
	u9 = User('User 9', [g])

	print(users := [u0, u1, u2, u3, u4, u5, u6, u7, u8, u9])
	print()

	c0 = Candidate(u0)
	c1 = Candidate(u1)
	c2 = Candidate(u2)
	c3 = Candidate(u3)
	c4 = Candidate(u4)
	c5 = Candidate(u5)
	
	print(candidates := [c0, c1, c2, c3, c4, c5])
	print()

	b0 = Ballot(agreement=Ranking([[c0, c1], [], [c2]]), disagreement=Ranking([[c4], [c5]]))
	b1 = Ballot(agreement=Ranking([[c1], [c4], [c2]]), disagreement=Ranking([[c5], [], [c3]]))
	b2 = Ballot(agreement=Ranking([[c5], [c4]]), disagreement=Ranking([[c0, c1, c3]]))
	b3 = Ballot(agreement=Ranking([[c1]]), disagreement=Ranking([[c0, c2, c3, c4, c5]]))

	print(ballots := [b0, b1, b2, b3])
	print()	
	
	print(election := Election(g, candidates, ballots))
	print()

	print(count := election.count())
	print()

	print(consensus := election.consensus())
	print()

	print(CandidateScoringSchema().dumps(count))
	print()

	print(CandidateScoringSchema().dumps(consensus))
	print()

	print(ElectionPollSchema().dumps(election))
	print()


	