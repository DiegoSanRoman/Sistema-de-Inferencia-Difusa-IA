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

# ------------------------- STEP 3: RULES EVALUATION -------------------------
risk_levels = {}
for app in applications:
    # Initialize a dictionary to store the risk levels for each rule
    rule_risks = {}
    for rule in rules:
        # Check if all antecedents of the rule are applicable to the application
        if all(antecedent in membership_degrees[app.appId] for antecedent in rule.antecedent):
            # Get the membership degrees for the antecedents of the rule
            antecedent_degrees = [membership_degrees[app.appId][antecedent] for antecedent in rule.antecedent]
            # Calculate the rule's strength as the minimum of these membership degrees
            rule_strength = min(antecedent_degrees)
            # Update the risk level for the rule using the rule's consequent and strength
            rule_risks[rule.ruleName] = min(rule_strength, skf.interp_membership(riskLevels[rule.consequent].x, riskLevels[rule.consequent].y, rule_strength))
    # Update the risk levels for the application using the maximum risk level from all the rules
    risk_levels[app.appId] = max(rule_risks.values()) if rule_risks else 0

# We print for checking
for app_id, risk_level in risk_levels.items():
    print(f"Application ID: {app_id}, Risk Level: {risk_level}")

# ------------------------- STEP 4: DEFFUZIFICATION -------------------------
risk_levels_defuzz = {}
for app in applications:
    # Get the risk level for the application
    risk_level = risk_levels[app.appId]
    # Calculate the defuzzified risk level using the centroid method
    risk_level_defuzz = skf.defuzz(riskLevels[rule.consequent].x, riskLevels[rule.consequent].y, 'centroid')
    risk_levels_defuzz[app.appId] = risk_level_defuzz

# Open the file in write mode
with open('results.txt', 'w') as file:
    # Iterate over the risk levels
    for app_id, risk_level_defuzz in risk_levels_defuzz.items():
        # Write the application ID and the defuzzified risk level to the file
        file.write(f"Application ID: {app_id}, Defuzzified Risk Level: {risk_level_defuzz}\n")