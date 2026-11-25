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

""" ----------------------------------------------------------------------------
**** Αναπαράσταση κατάστασης

  state = [θέση ρομπότ, δέματα 1ης θέσης, δέματα 2ης θέσης, δέματα 3ης θέσης,
           δέματα 4ης θέσης, δέματα 5ης θέσης, δέματα στο ρομπότ]

  θέση ρομπότ        : 0 = είσοδος, 1..5 = θέσεις αποθήκευσης
  δέματα i θέσης     : [kg 1ου δέματος, kg 2ου δέματος, ...], 0 = το δέμα έχει φορτωθεί
  δέματα στο ρομπότ  : [πλήθος δεμάτων, kg δεμάτων, πληρότητα (0 ή 1)]

  π.χ. αρχική κατάσταση εκφώνησης:
       [0, [12,15], [8,11], [3,9,7], [6,2,13], [10,4], [0,0,0]]
"""

NUM_POSITIONS = 5 # θέσεις αποθήκευσης 1..5(η 0 είναι η είσοδος)


# ******** Operators
# ******** Τελεστές

  
'''
Τελεστής move_left (δόθηκε από το εργαστήριο, δεν αλλάξαμε τη λογική του)
Προϋποθέσεις: το ρομπότ είναι σε θέση 2..5 (αριστερά υπάρχει θέση αποθήκευσης)
              και δεν είναι γεμάτο (πληρότητα = 0).
Αποτέλεσμα  : το ρομπότ πάει μία θέση αριστερά και εξετάζει με τη σειρά τα δέματα
              της νέας θέσης. Φορτώνει όσα χωράνε. Στο πρώτο δέμα που δεν χωράει
              (ήδη 3 δέματα ή πάνω από 20 kg) σηκώνει τη σημαία πληρότητας και σταματά.
'''
def move_left(state):
    if state[0]>1 and state[-1][2]==0: # υπάρχει θέση αριστερά και δεν είναι γεμάτο
        state[0]=state[0]-1 # μετακίνηση μία θέση αριστερά
        
        for i in range(len(state[state[0]])): # τα δέματα της νέας θέσης με τη σειρά
            parcel=state[state[0]][i]

            if parcel>0: # 0 = το δέμα έχει ήδη φορτωθεί
                if state[-1][0]<3 and state[-1][1]+parcel<=20: # χωράει (<3 δέματα, <=20 kg)
                    state[-1][0]=state[-1][0]+1 # ένα δέμα παραπάνω στο ρομπότ
                    state[-1][1]=state[-1][1]+parcel # και το βάρος του
                    state[state[0]][i]=0 # το δέμα φεύγει από τη θέση
                else:
                    state[-1][2]=1 # παραβίαση περιορισμού -> γεμάτο
                    break # δεν εξετάζει τα επόμενα δέματα

        if state[-1][0]==3: # με 3 δέματα είναι σίγουρα γεμάτο
            state[-1][2]=1

        return state


'''
Τελεστής move_right (συμμετρικός του move_left)
Προϋποθέσεις: το ρομπότ είναι στην είσοδο ή σε θέση 1..4 (δεξιά υπάρχει θέση)
              και δεν είναι γεμάτο (πληρότητα = 0).
Αποτέλεσμα  : το ρομπότ πάει μία θέση δεξιά και φορτώνει με τον ίδιο κανόνα.
'''
def move_right(state):
    if state[0]<5 and state[-1][2]==0: # υπάρχει θέση δεξιά και δεν είναι γεμάτο
        state[0]=state[0]+1 # μετακίνηση μία θέση δεξιά

        for i in range(len(state[state[0]])): # τα δέματα της νέας θέσης με τη σειρά
            parcel=state[state[0]][i]

            if parcel>0:
                if state[-1][0]<3 and state[-1][1]+parcel<=20: # χωράει
                    state[-1][0]=state[-1][0]+1
                    state[-1][1]=state[-1][1]+parcel
                    state[state[0]][i]=0
                else:
                    state[-1][2]=1 # παραβίαση περιορισμού -> γεμάτο
                    break

        if state[-1][0]==3:
            state[-1][2]=1

        return state


'''
Τελεστής unload: επιστροφή στην είσοδο και εκφόρτωση (μία ενέργεια)
Προϋποθέσεις (μία από τις δύο):
  α) το ρομπότ είναι γεμάτο (πληρότητα = 1). Τότε είναι και ο μόνος τελεστής που
     εφαρμόζεται (οι move_left/move_right θέλουν πληρότητα 0), άρα η επιστροφή
     γίνεται "αυτόματα", όπως λέει η εκφώνηση.
  β) δεν έχει μείνει κανένα δέμα στις θέσεις και η δουλειά δεν έχει τελειώσει
     (το ρομπότ κρατάει δέματα ή δεν είναι στην είσοδο). Χωρίς αυτή την περίπτωση
     το τελευταίο φορτίο δεν θα έφτανε ποτέ στην είσοδο, αφού δεν θα υπήρχε
     επόμενο δέμα για να "γεμίσει" το ρομπότ.
Αποτέλεσμα  : το ρομπότ βρίσκεται στην είσοδο (θέση 0) και είναι άδειο [0,0,0].
'''
def unload(state):
    full=state[-1][2]==1
    finished=shelves_empty(state) and (state[-1][0]>0 or state[0]!=0)
 
    if full or finished:
        state[0]=0                                      # επιστροφή στην είσοδο
        state[-1]=[0,0,0]                               # εκφόρτωση όλων των δεμάτων
        return state

'''
Συνάρτηση εύρεσης απογόνων της τρέχουσας κατάστασης (συνάρτηση διαδόχων)
Εφαρμόζει κάθε τελεστή σε ξεχωριστό αντίγραφο της κατάστασης (deepcopy), ώστε να
μην αλλάξει η κατάσταση-γονέας, και κρατά μόνο όσους τελεστές εφαρμόστηκαν
(οι τελεστές επιστρέφουν None όταν δεν ισχύουν οι προϋποθέσεις τους).
Σειρά τελεστών: move_left, move_right, unload.
'''

def find_children(state):
    
    children=[]
    
    left_state=copy.deepcopy(state)
    left_child=move_left(left_state)

    right_state=copy.deepcopy(state)
    right_child=move_right(right_state)

    unload_state=copy.deepcopy(state)
    unload_child=unload(unload_state)
    
    if left_child!=None: 
        children.append(left_child)

    if right_child!=None:
        children.append(right_child)
        
    if unload_child!=None:
        children.append(unload_child)
    
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
"""

def shelves_empty(state):
    """True αν δεν έχει μείνει κανένα δέμα σε καμία από τις θέσεις 1..5."""
    for i in range(1, NUM_POSITIONS+1):
        for parcel in state[i]:
            if parcel>0:
                return False
    return True

""" Function that checks if current state is a goal state
    Συνάρτηση που ελέγχει αν μια κατάσταση είναι τελική:
    όλα τα δέματα έχουν φύγει από τις θέσεις, το ρομπότ είναι στην είσοδο και άδειο.
    Δεν συγκρίνουμε με μία σταθερή λίστα (π.χ. [0,[0,0],[0,0],...]), γιατί το σχήμα
    της τελικής κατάστασης εξαρτάται από το πόσα δέματα είχε κάθε θέση στην αρχή. """

def is_goal_state(state):
    return state[0]==0 and shelves_empty(state) and state[-1]==[0,0,0]

""" ----------------------------------------------------------------------------
**** Basic recursive function to create search tree (recursive tree expansion)
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""


def find_solution(front, queue, closed, method):
       
    if not front:
        print('_NO_SOLUTION_FOUND_')
    
    elif front[0] in closed:
        new_front=copy.deepcopy(front)
        new_front.pop(0)
        new_queue=copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, method)
    
    elif is_goal_state(front[0]):
        print('_GOAL_FOUND_')
        print(queue[0])
        
    else:
        closed.append(front[0])
        front_copy=copy.deepcopy(front)
        front_children=expand_front(front_copy, method)
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        closed_copy=copy.deepcopy(closed)
        find_solution(front_children, queue_children, closed_copy, method)
        
        
        
""" ----------------------------------------------------------------------------
** Executing the code
** κλήση εκτέλεσης κώδικα
"""
           
def main():
    
    initial_state = [0, [12,15], [8,11], [3,9,7], [6,2,13], [10,4], [0,0,0]] 
    method='DFS'
    
    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], method)
    
    
if __name__ == "__main__":
    main()
