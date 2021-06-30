# Note to self: python3 is interpreteter
import sys
import fileinput

# Dictionaries for learned variables, root variables, facts, and rules.
varL = {}
varR = {}
facts = {} # list of variables
rules = [] 


def getRuleConsequent(rule_ante):
    for rule in rules:
        if rule[0] == rule_ante:
            return rule[1]
    return False
def getRuleAntecedent(rule_cons):
    for rule in rules:
        if rule[1] == rule_cons:
            return rule[0]
    return False
'''
Uses forward chaining to apply all of the rules of the system to the facts of the system to
create newly formed facts. Continues until no new knowledge can be acquired from the
given rules. If I type this command, and then type ‘List’, I should see new learned rules
listed out. This command does not accept any parameters.
'''
def applyRule(rule):
    return solveP(rule)

def solveP(rule):
    # Solves each parenthesis problem (starting from the innermost / last pair).
    while rule.count("(") > 0:
        leftP = rule.rindex("(")
        rightP = rule[leftP:].index(")") + leftP
        parens = rule[leftP+ 1 : rightP] # inside the parenthesis (without surrounding parentheses)
        rule = rule.replace("(" + parens + ")", str(solve(parens))) 
    return solve(rule)

def solve(rule):
    # Base case: returns iff variables (letters) make up the rule
    if rule.isalpha(): 
        if (not facts.get(rule, False) ) and (rule == "True"):
            return True
        elif (not facts.get(rule, False) ) and (rule == "False"):
            return False
        else:
            return bool(facts.get(rule, False))
                  
    if rule.find("|") > -1:
        orL = rule.split("|", 1)
        return solve(orL[0]) or solve(orL[1])

    if rule.find("&") > -1:
        andL = rule.split("&", 1)
        return solve(andL[0]) and solve(andL[1])

    if rule.find("!") > -1:
        notS = rule.replace('!', '', 1) 
        return not solve(notS)
    
def learn():
    # Loops and learns the rules.
    for rule in rules:
   # Adds resulting learned variable to list of facts if rule is true.
        if applyRule(rule[0]):
            res = rule[1] # Gets correlating /resulting learned variable to the rule.
            facts[res] = varL[res] # Adds learned variable / result to facts..

def listCommand():
    print("Root Variables: ")
    for var, s in varR.items():
        print("\t" + var, '=', s)
    print("Learned Variables:")
    for var, s in varL.items():
        print("\t" + var, '=', s)
    print("Facts:")
    for var in facts.keys():
        print("\t" + var)
    print("Rules: ") 
    for rule in rules:
        print("\t" + rule[0], '->', rule[1])

def query(exp):
    print(str(queryFact(exp)).casefold())

# Helper for QueryFact; returns dict of parenthesis indices in a string.
def find_parens(s):
    toret = {}
    pstack = []
    for i, c in enumerate(s):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i
    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    return toret

# Helper for query
def queryFact(exp):
    # Returns if exp is a root and whether it is a fact.
    if varR.get(exp, False):
        return bool(facts.get(exp, False))
    # Returns true if exp is a rule and if its consequence exists and is a fact.
    if getRuleConsequent(exp) and facts.get(getRuleConsequent(exp), False):
        return True
    # Recurses and changes expression to the correlating rule if it is a learned variable but not a confirmed fact.
    if bool(varL.get(exp,False)):
        if getRuleAntecedent(exp):
            exp = getRuleAntecedent(exp)
            return queryFact(exp)
        else:
            return False
    
    # Handles parentheses
    rangeP = []
    if exp.count("(") > 0 or exp.count(")") > 0:
        if exp.count("(") != exp.count(")"):
            exp = exp.replace("(", "")
            exp = exp.replace(")", "")

            return queryFact(exp)

        parenS = find_parens(exp)
            
        # Removes surrounding ( ) if they are the first and last chracter.
        if parenS.get(0, False) and parenS[0] == (len(exp) - 1):
            exp = exp[1:len(exp) - 1] 
            parenS.pop(0) 
        # Gets range of indices within the expression's parenthesis.
        if bool(parenS):
            for k in parenS.keys():
                rangeP = rangeP + list(range(k,parenS[k]))
    # Recurses on operators outside of any parenthesis.
    i = -1
    for c in exp:
        i = i + 1
        if c == "|" and not i in rangeP:
            return queryFact(exp[:i]) or queryFact(exp[i+1:])
        if c == "&" and not i in rangeP:
            return queryFact(exp[:i]) and queryFact(exp[i+1:])
        if c == "!" and not i in rangeP:
            return not queryFact(exp[i+1:])


s = []
def why(exp):
    global s
    b = queryFact(exp)
    while exp.count("(") != exp.count(")"):
        diff = exp.count("(") - exp.count(")")
        if diff > 0:
            exp = exp.replace("(","", 1)
        elif diff < 0:
            exp = exp.replace(")","", 1) 
        else:
            break
    # Handles parentheses
    p1, p2 = "",""
    if exp.count("(") > 0 or exp.count(")") > 0:
        parenS = find_parens(exp)
        # Removes surrounding ( ) if they are the first and last chracter.
        while parenS.get(0, False) and parenS[0] == (len(exp) - 1):
            exp = exp[1:len(exp) - 1] 
            parenS.pop(0) 
            parenS = find_parens(exp)
            p1 = p1 + "("
            p2 = p2 + ")"

    if varR.get(exp, False):
        if b:
            s.append("I KNOW THAT " + p1 + convert(exp) + p2) 
            return True
        else: 
            s.append("I KNOW IT IS NOT TRUE THAT " + p1 + convert(exp) + p2)
            return False
           
    if varL.get(exp, False) or getRuleAntecedent(exp):
        if not getRuleAntecedent(exp):
            s.append("I KNOW IT IS NOT TRUE THAT " + p1 + convert(exp) + p2)
            return False  
        elif getRuleConsequent(exp):
            vl = getRuleConsequent(exp)
        else:
            vl = exp
            exp = getRuleAntecedent(vl)
        if b: 
            for rule in getRules(vl):
                if queryFact(rule): 
                    s.append("BECAUSE " + p1 + convert(exp) + p2 + " I KNOW THAT " + convert(vl))
                    return why(exp)
        else:
            for rule in getRules(vl):
                if not queryFact(rule):
                    s.append("BECAUSE " + p1 + convert(exp) + p2 + " I KNOW THAT " + convert(vl))
                    why(rule)
                return False
    i =  -1
    prev_c = ''
    in_parens = False
    for c in exp:
        if i > -1:
            prev_c = exp[i]
        i = i + 1

        # HANDLING NOTS
        if prev_c == "!":
                    # TODO: FIX
                    if exp[i:].isalpha():
                        if varR.get(c, False):
                            if facts.get(c, False):
                                s.append("I KNOW THAT " + p1 + convert(exp[i:]) + p2) # TODO: include the before not?
                                b = False
                            else:
                                s.append("I KNOW IT IS NOT TRUE THAT " + p1 + convert(exp[i:]) + p2)
                                b = True
                    if b:
                        s.append("I THUS KNOW THAT " + p1 + convert(exp[i-1:]) + p2)
                        return not why(exp[i:])
                    else:
                        s.append("THUS I CANNOT PROVE " + p1 + convert(exp[:i+1]) + p2)
                        return not why(exp[i:])


        # HANDLING PARENTHESIS
        if c == ")": 
            in_parens = False
            continue
        if in_parens:
            continue
        if c == "(":
            if exp[i+1:].find("(") > exp[i+1:].find(")"):
                in_parens = True
                why(exp[i:exp.find(")")+i+1])
            elif exp[i+1:].find("(") < exp[i+1:].find(")"):
                #why(exp[i+1:].find("(")exp.find(")")+i+1]) # FIX. 
                exp[i+1:].find("(") > exp[i+1:].find(")")
            continue


        if c == "|":
            if queryFact(exp[:i]) or queryFact(exp[i+1:]):
                if queryFact(exp[:i]):
                    s.append("I THUS KNOW THAT " + p1 + convert(exp[:i]) + " OR " + convert(exp[i+1:]) + p2)
                    return why(exp[:i])
                else: 
                    s.append("I THUS KNOW THAT " + p1 + convert(exp[:i]) + " OR " + convert(exp[i+1:]) + p2)
                    return why(exp[i+1:])
            elif not (queryFact(exp[:i]) or queryFact(exp[i+1:])):
                s.append("THUS I CANNOT PROVE "+  p1 + convert(exp[:i]) + " OR " + convert(exp[i+1:]) + p2)
                return why(exp[:i]) or why(exp[i+1:])
        if c == "&":
            if not queryFact(exp[:i]):
                s.append("THUS I CANNOT PROVE " + p1 + convert(exp[:i]) + " AND " + convert(exp[i+1:]) + p2)
                return why(exp[:i])
            elif not queryFact(exp[i+1:]): 
                s.append("THUS I CANNOT PROVE " + p1 + convert(exp[:i]) + " AND " + convert(exp[i+1:]) + p2)
                return why(exp[i+1:])
            else:
                s.append("I THUS KNOW THAT " + p1 + convert(exp[:i]) + " AND " + convert(exp[i+1:]) + p2)
                # switch statements?
                return why(exp[i+1:]) and why(exp[:i])
def convert(exp):
    s = ''
    for c in exp:
        if varR.get(c, False):
            s = s + varR[c]
        elif varL.get(c, False):
            s = s + varL[c]
        elif c == "&":
            s = s + " AND "
        elif c == "|":
            s = s + " OR "
        elif c == "!":
            s = s + "NOT "
        elif c == "(":
            s = s + "("
        elif c == ")":
            s = s + ")"
    return s.replace('"', '').strip(" ")

def getRules(vL):
    rulesVarL = []
    for rule in rules:
        if rule[1] == vL:
            rulesVarL.append(rule[0])
    return rulesVarL
        
def createNewVar(arg, var, s):
    # Returns if the variable already exists.
    if varR.get(var,False) or varL.get(var,False):
        return
    # Adds variable to root variables if arg is -R.
    elif arg == '-R':
        varR[var] = s

    # Adds variable to root variables if arg is -L.
    elif arg == '-L':
        varL[var] = s

def changeRootVal(var, b):
    # Needs to clear facts dictionary of learned variables
    for k in list(varL.keys()):
        if facts.get((k), False):
            facts.pop(k)
    if(b == 'true'):
        facts[var] = varR[var]
    elif facts.get(var, False):
        facts.pop(var)

'''Teaches the system a new rule. The antecedent may be an entire expression, but the
expression will only contain AND, OR, and NOT operators. The expression may contain
parentheses. All variable defined here must have already been defined via the previous
‘Teach’ command, otherwise you can ignore this command. There will be one space on
each side of the ‘->’ symbol. However, the expression defined as <EXP> will contain no
spaces. This <EXP> will also not be fully parenthesized (it might be) and will contain only !
(not), & (and), and | (or) symbols. If no parentheses, use the following order of
operations: Not, And, Or. The <EXP> may contain a mix of root and learned variables,
however the consequence <VAR> must be a learned variable.'''
def createNewRule(rule, res):
    # Loops through tokens to check that every variable exists.
    for tok in rule:
        # Continues to next token if current is a logic op or parenthesis. 
        if tok == "!" or tok == "&" or tok == "|" or tok == ")" or tok == "(":
            continue
        # Returns if token does not already exists as a variable.
        else:
            if not (varL.get(tok,False) or varR.get(tok, False)):
                return
    #  Adds (rule, result) to rules dictionary if result correlates to a learned variable.
    if varL.get(res):
        rules.append((rule, res))
# Goes through each command (line) in input. 
#for line in fileinput.input(): # TODO: Switch to 'correct' impl.
while(True):
    
    line = sys.stdin.readline()
    command = line.strip().split()[0]

    # Input will end with a single line containing a ‘0’. 
    if '0' == command: 
        break
    elif 'List' == command:
        listCommand()   
    elif 'Learn' == command:
        learn()
    elif 'Query' == command:
        query(
            line.strip().split()[1]
            ) 
    elif 'Why' == command:
        print(str(why(line.strip().split()[1])).casefold())
        s.reverse()
        for e in list(dict.fromkeys(s)):
            print(e)
        s = []
    elif 'Teach' == command:
        # New variable
        if line.strip().split()[1].find('-') > -1: # and line.find('=') > -1
            createNewVar(
                line.strip().split()[1], 
                line.strip().split()[2], 
                line.split("=")[1].strip()
                )
        # Sets new root variable and all variables to false.
        elif line.find('=') > -1 and varR.get(line.strip().split()[1], False):
            changeRootVal(
                line.strip().split()[1].strip(), 
                line.strip().split("=")[1].strip()
                ) 
        # Creates new rule
        elif line.find('->') > -1:
            createNewRule(
                line.strip().split()[1], 
                line.split("->")[1].strip()
                )


