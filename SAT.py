import re
import copy

def read(input_file):
    f = open(input_file, "r")
    inputs = re.split(r"[,]",f.readline().strip()) # reading the different variables
    number_of_factors = int(f.readline())  # reading the number of sum terms given
    clause_list = []
    # iterating to get each of the sum terms
    for n in range(number_of_factors):
        line = f.readline().strip()
        x = re.split(r"[+]",line)
        clause_list.append(x)
    return inputs, clause_list

sat = False
complete = False
inputs,list_clause = read('input.txt') # change the name of the input file here
print(inputs)
assgn_done = []
assgn = [False]*len(inputs)

def unit_clauses(clauses_in,assigned_in,assign_in):
    #assigned_in -- list of all literals that have been assigned
    #assign_in   -- to save the assigned value
    sat = False
    complete_in = False
    dummy = copy.deepcopy(clauses_in)
    for clause in dummy:
        if len(clause) == 1:
            if clause[0] in inputs:
                index = inputs.index(clause[0])
                if index in assigned_in and assign_in[index] == False: #the literal is already assigned with fase but should also be true, so SAT will be False
                    complete_in = True
                    sat = False    
                elif not(index in assigned_in): #Unassigned literal, so assigning it True
                    assign_in[index] = True
                    assigned_in.append(index)        
            else :
                index = inputs.index(clause[0][:-1])
                if index in assigned_in and assign_in[index] == True: #the literal is already assigned with fase but should also be false, so SAT will be False
                    complete_in = True
                    sat = False    
                elif not(index in assigned_in): #Unassigned literal, so assigning it False     
                    assign_in[index] = False
                    assigned_in.append(index) 

            index_clause = clauses_in.index(clause)
            del clauses_in[index_clause]
    
    return sat,clauses_in,assigned_in,assign_in,complete_in


#to find pure literals, I counted the number of x and x_bar in the clauses, 
#if any one of them was 0, it was a pure literal
def pure_literal(clauses_in,assigned_in,assign_in):
    
    for index in range(len(inputs)):
        dummy = copy.deepcopy(clauses_in)
        if not(index in assigned_in):
            x = inputs[index]
            x_count = 0
            x_bar = x + "'"
            x_bar_count = 0
            for clause in dummy:
                if x in clause and x_bar in clause:
                    index_clause = clauses_in.index(clause)
                    del clauses_in[index_clause]
                elif x in clause:
                    x_count = x_count+1
                elif x_bar in clause:
                    x_bar_count = x_bar_count + 1
            if x_count == 0:
                assign_in[index] = False
                assigned_in.append(index)
            elif x_bar_count == 0:
                assign_in[index] = True
                assigned_in.append(index)
            if index in assigned_in:
                for clause_check in dummy:
                    if x in clause_check or x_bar in clause_check:
                        index_clause_check = clauses_in.index(clause_check)
                        del clauses_in[index_clause_check]

    return clauses_in,assigned_in,assign_in

def brute(clauses_in,assigned_in,assign_in,index):
    if index == len(inputs):
        sat = False
        done = False
        return sat, done, assign_in
    dummy = copy.deepcopy(clauses_in)
    dummy_clauses_in1 = copy.deepcopy(clauses_in)
    dummy_clauses_in2 = copy.deepcopy(clauses_in)
    while index in assigned_in:
        index = index + 1
        if index == len(inputs):
            sat = False
            done = False
            return sat, done, assign_in
    if not(index in assigned_in):
        x = inputs[index]
        x_count = 0
        x_bar = x + "'"
        x_bar_count = 0
        for clause in dummy:
            if x in clause:
                x_count = x_count+1
            elif x_bar in clause:
                x_bar_count = x_bar_count + 1
        if x_count >= x_bar_count:
            assign_in[index] = True
            for clause_check in dummy:
                if x in clause_check:
                    index_clause_check = dummy_clauses_in1.index(clause_check)
                    del dummy_clauses_in1[index_clause_check]

        else:
            for clause_check in dummy:
                assign_in[index] = False
                if x_bar in clause_check:
                    index_clause_check = dummy_clauses_in1.index(clause_check)
                    del dummy_clauses_in1[index_clause_check]

        if len(dummy_clauses_in1) == 0:
            sat = True;
            done = True;
            return sat, done, assign_in

        sat,done,assign_in = brute(dummy_clauses_in1,assigned_in,assign_in,index+1)

        if done is not True:
            if x_count >= x_bar_count:
                assign_in[index] = False
                for clause_check in dummy:
                    if x_bar in clause_check:
                        index_clause_check = dummy_clauses_in2.index(clause_check)
                        del dummy_clauses_in2[index_clause_check]

            else:
                assign_in[index] = True
                for clause_check in dummy:
                    if x in clause_check:
                        index_clause_check = dummy_clauses_in2.index(clause_check)
                        del dummy_clauses_in2[index_clause_check]

            if len(dummy_clauses_in2) == 0:
                sat = True;
                done = True;
                return sat, done, assign_in

            sat,done,assign_in = brute(dummy_clauses_in2,assigned_in,assign_in,index+1)
        return sat,done,assign_in

def SAT():
    global sat
    global complete
    if sat :
        print (assgn)
        print("SAT")
    else:
        print("UNSAT")

sat,list_clause,assgn_done,assgn,complete = unit_clauses(list_clause,assgn_done,assgn)
if complete : 
    SAT()
else:
    list_clause,assgn_done,assgn = pure_literal(list_clause,assgn_done,assgn)
    if len(list_clause) == 0:
        print (assgn)
        print("SAT")
    else:
        sat,done,assgn= brute(list_clause,assgn_done,assgn,0)
        SAT()
