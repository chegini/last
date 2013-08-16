from z3 import *

inHole1 = Function('inHole1', IntSort(), IntSort(),BoolSort())
inHole2 = Function('inHole2', IntSort(), IntSort(),BoolSort())
s = Solver()

piegon = 3
hole = 3
a =[]

for p in range(piegon):
	for h1 in range(hole):
		for h2 in range(h1+1,hole):
		 
			a = a + [ Implies(inHole1(p,h1),Not(inHole1(p,h2)))]


s.add(a)
b =[]
for h in range(hole):
	for pp1 in range(piegon): 
		for pp2 in range(pp1+1,piegon):
			b = b + [Implies(inHole1(pp1,h),Not(inHole1(pp2,h)))]

s.add(b)

#s.add(Not(inHole1(2,2)))
c =[]
for pp in range(piegon):
	c = c + [ Or([inHole1(pp,h) for h in range(hole)])   ]

s.add(c)



#-------------------------------------------------------------

a = []
for h1 in range(hole): 
	for h2 in range(h1+1,hole):
		for p in range(piegon):
			a = a + [ Implies(inHole2(p,h1),Not(inHole2(p,h2)))]

s.add(a)

b = []
for pp1 in range(piegon): 
	for pp2 in range(pp1+1,piegon):
		for h in range(hole):
			b = b + [Implies(inHole2(pp1,h),Not(inHole2(pp2,h))) ]

s.add(b)

c = []
for pp in range(piegon):
	c = c + [ Or([inHole2(pp,h) for h in range(hole)])  ]

s.add(c)

#-------------------------------------------------------------


a = []
for h in range(hole): 
	for p in range(piegon):
		a = a + [ Implies(inHole1(p,h),inHole2(p,h))]
s.add(a)





print s.check()
if(s.check() == sat):
	m=s.model()
	print m
quit()







