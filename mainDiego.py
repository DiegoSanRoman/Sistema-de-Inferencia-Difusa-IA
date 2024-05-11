import numpy as np
import skfuzzy as skf
import matplotlib.pyplot as plt
from MFIS_Classes import *
from MFIS_Read_Functions import *

# -------------------------- STEP 1: READ FILES --------------------------
# Read fuzzy sets from file
fuzzySets = readFuzzySetsFile('InputVarSets.txt')
# fuzzySets.printFuzzySetsDict()
# Read risk levels from file
riskLevels = readFuzzySetsFile('Risks.txt')
# riskLevels.printFuzzySetsDict()
# Read rules from file
rules = readRulesFile()
# rules.printRuleList()
# Read applications from file
applications = readApplicationsFile()
#for app in applications:
    #app.printApplication()
# Fuzzify applications
for app in applications:
    for elem in app.data:
        var = elem[0]
        val = elem[1]
        for setid in fuzzySets:
            if fuzzySets[setid].var == var:
                fuzzySets[setid].memDegree = skf.interp_membership(fuzzySets[setid].x, fuzzySets[setid].y, val)
                break


# -------------------------- STEP 2: FUZZIFICATION --------------------------
# We plot the membership functions for each fuzzy set
for setid in fuzzySets:
    plt.plot(fuzzySets[setid].x, fuzzySets[setid].y, label=setid)
    plt.legend()
    plt.title('Membership functions')
    #plt.show()

# We plot the membership degrees for each application
for app in applications:
    app.printApplication()
    for elem in app.data:
        var = elem[0]
        val = elem[1]
        for setid in fuzzySets:
            if fuzzySets[setid].var == var:
                fuzzySets[setid].memDegree = skf.interp_membership(fuzzySets[setid].x, fuzzySets[setid].y, val)
                print(setid, fuzzySets[setid].memDegree\n)
                break

