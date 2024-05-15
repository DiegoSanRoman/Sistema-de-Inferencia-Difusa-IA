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
    for setid in fuzzySets:
        # analyze each application data
        for var, value in app.data:
            # if fuzzy variable matches app variable
            if fuzzySets[setid].var == var:
                # Calculate membership degree and provides fuzzy set
                # en vez de guardarlo en un diccionario lo he guardado directamente en el atributo del degree
                fuzzySets[setid].memDegree = skf.interp_membership(fuzzySets[setid].x, fuzzySets[setid].y, value)

    # ------------------------- STEP 3: RULES EVALUATION -------------------------
    # each possible risk level (range)
    appX = riskLevels[list(riskLevels.keys())[0]].x
    # 0's array with same length as appX
    appY = np.zeros_like(appX)
    for rule in rules:
        # Calculate strength of the antecedent
        rule.strength = 1
        for setid in rule.antecedent:
            rule.strength = min(rule.strength, fuzzySets[setid].memDegree)
        # Calculate the consequent
        rule.consequentX = riskLevels[rule.consequent].x
        rule.consequentY = riskLevels[rule.consequent].y
        rule.consequentY = np.minimum(rule.consequentY, rule.strength)
        # Accumulate output results
        appY = np.maximum(rule.consequentY, appY)

    # ------------------------- STEP 4: DEFUZZIFICATION -------------------------
    # calculate the centroid
    risk_centroid = skf.centroid(appX, appY)
    results_file.write(f"Application {app.appId}, Defuzzified Risk Level: {risk_centroid}\n")

results_file.close()
