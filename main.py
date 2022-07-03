from datetime import datetime
from uuid import uuid4
from permission import Permission
from group import Group
from user import User
from candidate import Candidate
from ballot import Ballot
from ranking import Ranking

from pprint import pformat

from group import Group

from election import Election
import json
from entity import Entity

from copy import deepcopy, copy

if __name__ == '__main__':

	p = Permission(read=False, write=False, execute=False)
	ps = [p]

	g = Group(name='Group 0', permissions=ps)
	gs = [g]

	u0 = User(name='User 0', groups=gs)
	u1 = User(name='User 1', groups=gs)
	u2 = User(name='User 2', groups=gs)
	u3 = User(name='User 3', groups=gs)
	u4 = User(name='User 4', groups=gs)
	u5 = User(name='User 5', groups=gs)
	u6 = User(name='User 6', groups=gs)
	u7 = User(name='User 7', groups=gs)
	u8 = User(name='User 8', groups=gs)
	u9 = User(name='User 9', groups=gs)

	print(users := [u0, u1, u2, u3, u4, u5, u6, u7, u8, u9])
	print()

	c0 = Candidate(user=u0)
	c1 = Candidate(user=u1)
	c2 = Candidate(user=u2)
	c3 = Candidate(user=u3)
	c4 = Candidate(user=u4)
	c5 = Candidate(user=u5)
	
	print(candidates := [c0, c1, c2, c3, c4, c5])
	print()

	b0 = Ballot(agreement=Ranking(ranks=[[c0, c1], [c2]]), disagreement=Ranking(ranks=[[c4], [c5]]))
	b1 = Ballot(agreement=Ranking(ranks=[[c1], [c4], [c2]]), disagreement=Ranking(ranks=[[c5]]))
	b2 = Ballot(agreement=Ranking(ranks=[[c5], [c4]]), disagreement=Ranking(ranks=[]))
	b3 = Ballot(agreement=Ranking(ranks=[[c1]]), disagreement=Ranking(ranks=[[c0, c2]]))

	print(ballots := [b0, b1, b2, b3])
	print()	
	
	print(election := Election(group=g, voters=users, candidates=candidates))
	print()

	election.ballots = ballots

	print(count := election.count())
	print()

	print(consensus := election.consensus())
	print()
