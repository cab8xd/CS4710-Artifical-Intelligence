# Note to self: python3 is interpreteter
import sys
import fileinput

# Dictionaries for learned variables, root variables, facts, and rules.
varL = {}
varR = {}
facts = {}
rules = {}

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
        # print(parens)
        if (parens.find(")") > -1) or (parens.find(")") > -1): 
            print("ERROR: parens in parens (where parens should not beee.)")
        # Replaces parenthesis with solution.
        rule = rule.replace("(" + parens + ")", str(solve(parens))) 
        # print("new rule " + rule)
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
    #print("Learning...")
    # Loops and learns the rules.
    for rule in rules.keys():
        #print("iterating on rule: " + rule)

        # Adds resulting learned variable to list of facts if rule is true.
        if applyRule(rule):
            res = rules[rule] # Gets correlating /resulting learned variable to the rule.
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
    for ch, con in rules.items():
        print("\t" + ch, '->', con)

def query(exp):
    print(str(queryFact(exp)).casefold())

# Helper for QueryFact; returns dict of parenthesis indices in a string.
def find_parens(s):
    toret = {}
    pstack = []
   # print(s)
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
    if rules.get(exp, False) and facts.get(rules.get(exp), False):
            return True
    # Recurses and changes expression to the correlating rule if it is a learned variable but not a confirmed fact.
    if bool(varL.get(exp,False)):
        rulesRev = dict(zip(rules.values(),rules.keys()))
        if rulesRev.get(exp, False):
            exp = rulesRev[exp]
            return queryFact(exp)
        else:
            return False
    
    # Handles parentheses
    rangeP = []
    if exp.count("(") > 0:
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



co_list = ''
counter = 0
def why(exp):
    print(exp)
    global counter
    global co_list
    b = queryFact(exp)
    ret1 = ""
    ret2 = ""
    if varR.get(exp, False):
        if b:
            ret = ret + "True "
            ret2  = ret2 + varR.get(exp) + " "
            print("I KNOW THAT " + varR.get(exp)) 
        else:
            ret = ret + "False "
            ret2  = ret2 + varR.get(exp) + " "
            print("I KNOW IT IS NOT TRUE " + varR.get(exp))
    else:
        rule = None
        for r in rules.keys():
            if rules[r] == exp:
                rule = r
                break
        if rule:
            ruleRet = why(rule)
            if queryFact(ruleRet[0]):
                ret1 = ret1 + "True "
                ret2 = ret2 + varL[exp] + " "
                print("BECAUSE " + ruleRet[1] + "I KNOW THAT " + varL[exp])
            else:
                ret1 = ret1 + "False "
                ret2 = ret2 + varL[exp] + " "
                print("BECAUSE IT IS NOT TRUE THAT " + ruleRet[1] + "I CANNOT PROVE " + varL[exp])
        else:
            print("else")
            if(counter > 0) and (co_list[counter-1] == "!"):
                print("I KNOW IT IS NOT TRUE THAT " + varR.get(exp, "") + varL.get(exp, ""))
                ret1 = ret1 + "False "
                ret2 = ret2 +  varR.get(exp, "") + varL.get(exp, "") + " "
        counter = counter + 1
    ret1 = convert(ret1)
    ret2 = convert(ret2)
    return [ret1, ret2]

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
            s = s + "OR "
        elif c == "!":
            s = " NOT " + s
        elif c == "(":
            s = "(" + s
        elif c == ")":
            s = s + ")"
    return s.replace('"', '').strip(" ")

def getRules(vL):
    rulesVarL = []
    for k in rules.keys():
        if rules[k] == vL:
            rulesVarL.append(k)
    return rulesVarL
        
def createNewVar(arg, var, s):
    # print("Creeating variable... ")
    # print("arg: " + arg)
    # print("var: " + var)
    # print("str: " + s)

    # Returns if the variable already exists.
    if varR.get(var,False) or varL.get(var,False):
        print("ERROR: variable already exists.")
        return
    # Adds variable to root variables if arg is -R.
    elif arg == '-R':
        varR[var] = s

    # Adds variable to root variables if arg is -L.
    elif arg == '-L':
        varL[var] = s

    # Prints error message if arg is not recognized.
    else:
        print("ERROR: arg not recognized.")
    # print("...Done.")

def changeRootVal(var, b):
    # Needs to clear facts dictionary of learned variables
    for v in list(varL.values()):
        if facts.get(v, False):
            facts.pop(v)

    # Adds root variable to facts if true input.
    if(b == 'true'):
        facts[var] = varR[var]
    # print("...Done.")

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

        # print("Looping on token: " + tok)

        # Continues to next token if current is a logic op or parenthesis. 
        if tok == "!" or tok == "&" or tok == "|" or tok == ")" or tok == "(":
            continue

        # Returns if token does not already exists as a variable.
        else:
            if not (varL.get(tok,False) or varR.get(tok, False)):
                print("Variable nonexistent; ignoring new rule.")
                return

    #  Adds (rule, result) to rules dictionary if result correlates to a learned variable.
    if varL.get(res):
        rules[rule] = res

    else:
        print("ERROR: res not a learned variable.")

    # print("...Done.")

# Goes through each command (line) in input. 
for line in fileinput.input(): # TODO: Switch to 'correct' impl.
#while(True):
    
    #line = sys.stdin.readline()
    command = line.strip().split()[0]
    # print("INPUT: " + line)

    # Input will end with a single line containing a ‘0’. 
    if '0' == command: 
        # print("DONE.")
        # print("=============")
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
        counter = 0
        co_list = line.strip().split()[1]
        print(str(why(line.strip().split()[1])).casefold())
        #s.reverse()
        #for e in s:
        #    print(e)
        #s = []

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

    else:
        print("Error: command not recognized.")



