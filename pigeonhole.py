#!/usr/bin/env python

# !!! Change this to fit your path !!!

minisat="/Users/ernst/Dropbox/SHARED/Fatem/MINISAT/minisat/core/minisat"

import sys
from subprocess import Popen
from subprocess import PIPE
import re
import random
import os

gbi = 0
varToStr = ["invalid"]

def printClause(cl):
    print map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval ("''"), varToStr[abs(x)]) , cl)

def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi

def gen_vars():

    varMap = {}
    TIME = 3
    MAX = 3
    S = ["E","+","n"]
    R = [1,2]
    for t in range(0,TIME):
        for i in range(0,MAX):
            for s in S:
                varMap["symbol1(%s,%d,%d)" % (s,i,t)] = gvi("symbol1(%s,%d,%d)" % (s,i,t))
            for r in R:    
                varMap["transition1(%d,%d,%d)" % (r,i,t)] = gvi("transition1(%d,%d,%d)" % (r,i,t))





    return varMap

def genPigConstr(vars):

    clauses = []

    TIME = 3
    MAX = 3
    S = 3

    for t in range(0,TIME-1):
        for i in range(0,MAX):
            a =  vars["symbol1(n,%d,%d)" % (i,t+1)]
            b =  vars["transition1(1,%d,%d)" % (i,t)]
            c = [-a,-b]
            clauses.append([-vars["symbol1(E,%d,%d)" % (i,t)]]+ c)

                

    return clauses

# A helper function to print the cnf header
def printHeader(n):
    global gbi
    return "p cnf %d %d" % (gbi, n)

# A helper function to print a set of clauses cls
def printCnf(cls):
    return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))

# This function is invoked when the python script is run directly and not imported
if __name__ == '__main__':
    if not (os.path.isfile(minisat) and os.access(minisat, os.X_OK)):
        print "Set the path to minisat correctly on line 4 of this file (%s)" % sys.argv[0]
        sys.exit(1)

    # This is for reading in the arguments.
    if len(sys.argv) != 3:
        print "Usage: %s <pigeons> <holes>" % sys.argv[0]
        sys.exit(1)

    pigeons = int(sys.argv[1])
    holes = int(sys.argv[2])

    vars = gen_vars()
    #print vars
  
    rules = genPigConstr(vars)
    #print rules
    head = printHeader(len(rules))
    rls = printCnf(rules)
   
    # here we create the cnf file for minisat
    fl = open("tmp_prob.cnf", "w")
    fl.write("\n".join([head, rls]))
    fl.close()

    # this is for runing minisat
    ms_out = Popen([minisat, "tmp_prob.cnf", "solution"], stdout=PIPE).communicate()[0]

    # Print the output, just out of curiosity
    print ms_out

    # minisat with these arguments writes the solution to a file called "solution".  Let's check it
    res = open("solution", "r").readlines()

    # if it was satisfiable, we want to have the assignment printed out
    if res[0] == "SAT\n":
        print "helo"
        # First get the assignment, which is on the second line of the file, and split it on spaces
        asgn = map(int, res[1].split())
        # Then get the variables that are positive, and get their names.
        # This way we know that everything not printed is false.
        # The last element in asgn is the trailing zero and we can ignore it
        facts = map(lambda x: varToStr[abs(x)], filter(lambda x: x > 0, asgn[:-1]))

        for f in facts:
            print f

