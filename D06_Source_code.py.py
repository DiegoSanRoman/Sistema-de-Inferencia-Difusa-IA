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
# Process all the applications and write Results file
results_file = open('Results.txt', "w")

for app in applications:
    # -------------------------- STEP 2: FUZZIFICATION --------------------------
    for var, value in app.data:
        for setid in fuzzySets:
            if fuzzySets[setid].var == var:
                fuzzySets[setid].memDegree = skf.interp_membership(fuzzySets[setid].x, fuzzySets[setid].y, value)

    # ------------------------- STEP 3: RULES EVALUATION -------------------------
    appX = riskLevels[list(riskLevels.keys())[0]].x
    appY = np.zeros_like(appX)
    for rule in rules:
        # Initialize the strength of the rule to 1
        rule.strength = 1

        # Evaluate each condition in the antecedent separately
        antecedent_strengths = []
        for condition_group in rule.antecedent:
            # For each group of conditions separated by AND operator
            and_strengths = []
            for condition in condition_group:
                # Split the condition into variable and label
                variable, label = condition.split('=')
                # Find the fuzzy set corresponding to the condition
                fuzzy_set = next(
                    (fuzzy for fuzzy in fuzzySets.values() if fuzzy.var == variable and fuzzy.label == label), None)
                if fuzzy_set:
                    # Calculate the membership degree and append it to the list
                    and_strengths.append(skf.interp_membership(fuzzy_set.x, fuzzy_set.y, app.data[variable]))
            # Take the minimum value of the AND conditions
            antecedent_strengths.append(min(and_strengths))

        # Take the maximum value of the OR conditions
        rule.strength = max(antecedent_strengths)

    # ------------------------- STEP 4: DEFUZZIFICATION -------------------------
    risk_centroid = skf.centroid(appX, appY)
    results_file.write(f"Application {app.appId}, Defuzzified Risk Level: {risk_centroid}\n")
    print(f"Application {app.appId}, Defuzzified Risk Level: {risk_centroid}\n")
results_file.close()

