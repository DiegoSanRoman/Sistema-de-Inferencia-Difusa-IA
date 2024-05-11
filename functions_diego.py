import numpy as np
import skfuzzy as skf
import matplotlib.pyplot as plt
from MFIS_Classes import *
from MFIS_Read_Functions import *

# -------------------------- STEP 1: READ FILES --------------------------
# Read fuzzy sets from file
fuzzySets = readFuzzySetsFile('InputVarSets.txt')
# Read risk levels from file
riskLevels = readFuzzySetsFile('Risks.txt')
# Read rules from file
rules = readRulesFile()
# Read applications from file
applications = readApplicationsFile()
# -------------------------- STEP 2: FUZZIFICATION --------------------------
membership_degrees = {}
for app in applications:
    #Dictionary for each application
    application_membership = {}
    for elem in app.data:
        #Create a list for each variable
        each_variable_membership = []
        variable = elem[0]
        value = elem[1]
        # Search for all fuzzy sets for that variable
        fuzzy_sets_for_variable = [fuzzySets[setid] for setid in fuzzySets if fuzzySets[setid].var == variable]
        # Calculate and store the values for each one in the variable list
        for fuzzy_set in fuzzy_sets_for_variable:
            mem_degree = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, value)
            each_variable_membership.append(mem_degree)
        application_membership[variable] = each_variable_membership
    membership_degrees[app.appId] = application_membership

# We print for checking
for app_id, app_membership in membership_degrees.items():
    print(f"Application ID: {app_id}")
    # Iterate over each variable of the application
    for variable, membership_list in app_membership.items():
        print(f"Variable: {variable}")
        fuzzy_sets_for_variable = [fuzzySets[setid] for setid in fuzzySets if
                                   fuzzySets[setid].var == variable]
        # Now we iterate for each fuzzy set of that variable
        for i, mem_degree in enumerate(membership_list):
            print(f"  {fuzzy_sets_for_variable[i].label}: {mem_degree}")

# -------------------------- STEP 3: RULES ANALYSIS --------------------------
# We iterate for each rule and we need to analize it to see the final value
for setid in fuzzySets:
    plt.plot(fuzzySets[setid].x, fuzzySets[setid].y, label=setid)
    plt.legend()
    plt.title('Membership functions')
    plt.show()

