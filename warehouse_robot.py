""" ----------------------------------------------------------------------------
******** Search Code for DFS  and other search methods
******** (expanding front only)
******** author:  AI lab
********
******** Κώδικας για α DFS και άλλες μεθόδους αναζήτησης
******** (επέκταση μετώπου μόνο)
******** Συγγραφέας: Εργαστήριο ΤΝ
"""

import copy

 

# ******** Operators
# ******** Τελεστές

  
def move_left(state):
    if state[0]>1 and state[-1][2]==0: 
        state[0]=state[0]-1
        
        for i in range(len(state[state[0]])):
            parcel=state[state[0]][i]

            if parcel>0:
                if state[-1][0]<3 and state[-1][1]+parcel<=20:
                    state[-1][0]=state[-1][0]+1
                    state[-1][1]=state[-1][1]+parcel
                    state[state[0]][i]=0
                else:
                    state[-1][2]=1
                    break

        if state[-1][0]==3:
            state[-1][2]=1

        return state
 

'''
Συνάρτηση εύρεσης απογόνων της τρέχουσας κατάστασης
'''
def find_children(state):
    
    children=[]
    
    left_state=copy.deepcopy(state)
    left_child=move_left(left_state)
    
    if  left_child!=None: 
        children.append( left_child)
        
    
    
    
    return children



""" ----------------------------------------------------------------------------
**** FRONT
**** Διαχείριση Μετώπου
"""

""" ----------------------------------------------------------------------------
** initialization of front
** Αρχικοποίηση Μετώπου
"""

def make_front(state):
    return [state]
    
""" ----------------------------------------------------------------------------
**** expanding front
**** επέκταση μετώπου    
"""

def expand_front(front, method):  
    if method=='DFS':        
        if front:
            print("Front:")
            print(front)
            node=front.pop(0)
            for child in find_children(node):     
                front.insert(0,child)
    
    #elif method=='BFS':
    #elif method=='BestFS':
    #else: "other methods to be added"        
    
    return front


""" ----------------------------------------------------------------------------
**** QUEUE
**** Διαχείριση ουράς
"""

""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""

def make_queue(state):
    return [[state]]

""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""

def extend_queue(queue, method):
    if method=='DFS':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0,path)
    
    #elif method=='BFS':
    #elif method=='BestFS':
    #else: "other methods to be added" 
    
    return queue_copy


""" ----------------------------------------------------------------------------
**** Problem depending functions
**** ο κόσμος του προβλήματος (αν απαιτείται) και υπόλοιπες συναρτήσεις σχετικές με το πρόβλημα

  #### to be  added ####
"""

""" Function that checks if current state is a goal state """

#def is_goal_state(state):

""" ----------------------------------------------------------------------------
**** Basic recursive function to create search tree (recursive tree expansion)
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""

def find_solution(front, queue, closed, goal, method):
#def find_solution(front, queue, closed, method):
       
    if not front:
        print('_NO_SOLUTION_FOUND_')
    
    elif front[0] in closed:
        new_front=copy.deepcopy(front)
        new_front.pop(0)
        new_queue=copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, goal, method)
        #find_solution(new_front, new_queue, closed, method)
    
    #elif is_goal_state(front[0]):
    elif front[0]==goal:
        print('_GOAL_FOUND_')
        #print(front[0])
        print(queue[0])
        
    else:
        closed.append(front[0])
        front_copy=copy.deepcopy(front)
        front_children=expand_front(front_copy, method)
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        closed_copy=copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, goal, method)
        #find_solution(front_children, queue_children, closed_copy, method)
        
        
        
"""" ----------------------------------------------------------------------------
** Executing the code
** κλήση εκτέλεσης κώδικα
"""
           
def main():
    
    initial_state = [0, [12,15], [8,11], [3,9,7], [6,2,13], [10,4], [0,0,0]] 
    """ ----------------------------------------------------------------------------
    **** [Θέση ρομπότ, δέματα 1ης θέσης, δέματα 2ης θέσης, δέματα 3ης θέσης, δέματα 4ης θέσης, 
          δέματα 5ης θέσης, δέματα στο ρομπότ]
    δέματα i θέσης: [kg 1ου δέματος, kg 2ου δέματοε...]
    δέματα στο ρομπότ: [πλήθος δεμάτων, kg δεμάτων, πληρότητα(0 ή 1)]
    """
    goal = [0, [0,0], [0,0], [0,0,0], [0,0,0], [0,0], [0,0,0]]
    method='DFS'
    
    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)
    #find_solution(make_front(initial_state), make_queue(initial_state), [], method)
    
    
if __name__ == "__main__":
    main()
