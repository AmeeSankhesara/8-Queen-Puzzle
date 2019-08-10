#Amee Sankhesara
#Compile: python3 8puzzle.py
#heuristics used:
#1.Manhattan distance
#2.Eucledian distance 
#3.Misplaced tiles

import math

#maximum number of moves
max_moves = 8000

# goal state
goalState = [[1,2,3],
               [4,5,6],
               [7,8,0]]

#stores the results of A* and bfs for 3 heuristics
Final_Output = [[0,0,0],[0,0,0]]


#value is obtained , else returns -1
def index(i, seq):
    if i in seq:
        return seq.index(i)
    else:
        return -1

class EightPuzzle:

    def __init__(self):
        self.parentNode = None #parent node 
        self.ValueOfHeuristic = 0 #value for the heuristic function
        self.depth = 0 # depth of the current instance
        self.cloned_matrix = [] #initialize matrix to goal state so that we can clone and swap as per the requirement.
        for i in range(3):
            self.cloned_matrix.append(goalState[i][:])

    #generates list of list with possible moves for interchanging swaps
    def possible_moves(self):
        #findValue(0) finds the index of 0/blank to make possible moves
        row, col = self.findValue(0)
    
        #MatrixOfPossibleMoves list stores the index of possible moves/swaps 
        #initially, it stores the index of 0/blank with which other values can be swapped
        MatrixOfPossibleMoves = []
        
        # finds the index of next movable positions in the matrix
        if row > 0:
            MatrixOfPossibleMoves.append((row - 1, col))
        if col > 0:
            MatrixOfPossibleMoves.append((row, col - 1))
        if row < 2:
            MatrixOfPossibleMoves.append((row + 1, col))
        if col < 2:
            MatrixOfPossibleMoves.append((row, col + 1))

        return MatrixOfPossibleMoves
    
    def cloneMatrix(self):
        p = EightPuzzle()
        for i in range(3):
            p.cloned_matrix[i] = self.cloned_matrix[i][:]
        return p   

    def generate_possible_position(self):
        MatrixOfPossibleMoves = self.possible_moves()
        #zero stores the index of 0 in the matrix like (2,2)
        zero = self.findValue(0)
        #after this control goes to return and then calls swap_and_clone function

        def swap_and_clone(a, b):
            p = self.cloneMatrix()
            p.swapValue(a,b)
            p.depth = self.depth + 1
            p.parentNode = self
            return p

        #Ex: return map->[8->[2,2],[(1,2),(2,1)]]
		#(key,value) values-stores the possible locations 

        return map(lambda pair: swap_and_clone(zero, pair), MatrixOfPossibleMoves)

    #recursive function to store the solution path from the parent node
    def solutionPath(self, path):
        if self.parentNode == None:
            return path
        else:
            path.append(self)
            return self.parentNode.solutionPath(path)
    
    #overriding the existing function to get use of constructors    
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.cloned_matrix == other.cloned_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.cloned_matrix[row]))
            res += '\r\n'
        return res   

    #Performs BFS for goal state
    def BFS (self, heuristicFunction):
        
        def isSolved(puzzle):   
            return puzzle.cloned_matrix == goalState

        inputMatrixList = [self]
        intermediateMatrixList = []
        move_count = 0
        while len(inputMatrixList) > 0:
            x = inputMatrixList.pop(0)
            #move_count - increments the moves based on swap - no. of states , exits if it max_moves is reached
            move_count += 1

            if(move_count > max_moves):
                print ("Oops!! you didn't get a solution...")
                return [], move_count

            #x gets different matrices from pop based on different swaps performed
            if (isSolved(x)):
                if len(intermediateMatrixList) > 0:
                    return x.solutionPath([]), move_count
                else:
                    return [x]

            #generate_nextposible_position stores the map which has key,value of possible swaps for 0/blank
            generate_nextposible_position = x.generate_possible_position()
            #index_open for inputMatrixList and index_closed for closed list which stores x values
            idx_open = idx_closed = -1
            for move in generate_nextposible_position:
                #inputMatrixList - input matrix
                idx_open = index(move, inputMatrixList)
                idx_closed = index(move, intermediateMatrixList)
                hval = heuristicFunction(move)
                fval = hval

                if idx_closed == -1 and idx_open == -1:
                    move.ValueOfHeuristic = hval
                    inputMatrixList.append(move)
                elif idx_open > -1:
                    copy = inputMatrixList[idx_open]
                    if fval < copy.ValueOfHeuristic:
                        # copy move's values over existing
                        copy.ValueOfHeuristic = hval
                        copy.parentNode = move.parentNode
                elif idx_closed > -1:
                    copy = intermediateMatrixList[idx_closed]
                    if fval < copy.ValueOfHeuristic:
                        move.ValueOfHeuristic = hval
                        intermediateMatrixList.remove(copy)
                        inputMatrixList.append(move)

            intermediateMatrixList.append(x)
            inputMatrixList = sorted(inputMatrixList, key=lambda p: p.ValueOfHeuristic)

        # if the goal state is not reached, returns failure
        return [], move_count

    #Performs A* search for the goal state
    def AstarSearch(self, heuristicFunction):
     
        def isSolved(puzzle):
            return puzzle.cloned_matrix == goalState

        inputMatrixList = [self]
        intermediateMatrixList = []
        move_count = 0
        while len(inputMatrixList) > 0:
            x = inputMatrixList.pop(0)
            #print x
            move_count += 1

            if(move_count > max_moves):
                print ("Oops!! you didn't get a solution...")
                return [], move_count

            if (isSolved(x)):
                if len(intermediateMatrixList) > 0:
                    return x.solutionPath([]), move_count
                else:
                    return [x]
            #choose the possible option and then pass that to heuristic function.
            generate_nextposible_position = x.generate_possible_position()
            #check if both the list are empty.
            idx_open = idx_closed = -1
            for move in generate_nextposible_position:
                # check whether the node is already visited.
                idx_open = index(move, inputMatrixList)
                idx_closed = index(move, intermediateMatrixList)
                hval = heuristicFunction(move)
                #f(n) = g(n) + h(n) is performed below.
                fval = hval + move.depth

                if idx_closed == -1 and idx_open == -1:
                    
                    move.ValueOfHeuristic = hval
                    inputMatrixList.append(move)
                elif idx_open > -1:
                    
                    copy = inputMatrixList[idx_open]
                    if fval < copy.ValueOfHeuristic + copy.depth:
                        # copy move's values over existing
                        copy.ValueOfHeuristic = hval
                        copy.parentNode = move.parentNode
                        copy.depth = move.depth
                elif idx_closed > -1:
                    
                    copy = intermediateMatrixList[idx_closed]
                    if fval < copy.ValueOfHeuristic + copy.depth:
                        move.ValueOfHeuristic = hval
                        intermediateMatrixList.remove(copy)
                        inputMatrixList.append(move)

            intermediateMatrixList.append(x)
            inputMatrixList = sorted(inputMatrixList, key=lambda p: p.ValueOfHeuristic + p.depth)

        # if the goal state is not reached, returns failure
        return [], move_count

    def init_Matrix(self, values):
    	i=0;
    	for row in range(3):
            for col in range(3):
                self.cloned_matrix[row][col] = int(values[i])
                i=i+1

    #returns the row and column index of the specified values
    def findValue(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.cloned_matrix[row][col] == value:
                    return row, col

    #returns the value at the specified row and column   
    def getValue(self, row, col):        
        return self.cloned_matrix[row][col]

    #sets the value at the specified row and column
    def setValue(self, row, col, value):        
        self.cloned_matrix[row][col] = value

    #swaps values at the specified coordinates
    def swapValue(self, pos_a, pos_b):
        temp = self.getValue(*pos_a)
        self.setValue(pos_a[0], pos_a[1], self.getValue(*pos_b))
        self.setValue(pos_b[0], pos_b[1], temp)

#heuristicFunction template that provides the total steps from current and target position for each number and the total function.
def heuristic(puzzle, item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.getValue(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0: 
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

#heuristic 1 |x2-x1|+ |y2-y1|
def h_manhattan_distance(puzzle):
    return heuristic(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

#heuristic 2 - it is the sqaureroot of x2-x1 and y2-y1
def h_euclidean_distance(puzzle):
    return heuristic(puzzle,
                lambda r, tr, c, tc: math.sqrt((tr - r)**2 + (tc - c)**2),
                lambda t: t)

#heuristic 3
def h_misplaced_tiles(puzzle):
    return heuristic(puzzle,
                lambda r, tr, c, tc: misplaced_tiles_count(puzzle),
                lambda t: t)

def misplaced_tiles_count(puzzle):
    count = 0
    for row in range(3):
        for col in range(3):
            if (puzzle.getValue(row, col) != goalState[row][col]):
                count= count + 1
    return count

def main():
    input_matrix=[]

    for i in list(range(5)):
        input_matrix.append(input("Enter your 8-puzzle input string: "))
        
    print ("\nBelow are the given inputs for calculating average: ") 
    for j in list(range(len(input_matrix))):
        print("input -",j+1,"=",input_matrix[j])    
        
    print("\nBest First Search : ")    
    print("\nBFS with heuristic-1 Manhattan distance :")    
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_BFS_Manhattan_distance(p);
        
    print("\nBFS with heuristic-2 Euclidean distance :")  
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_BFS_Euclidean_distance(p);    
    
    print("\nBFS with heuristic-3 Mispalced tiles :")      
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_BFS_Misplaced_tiles(p);           
         
    print("\nA* search : ")    
    print("\nA* with heuristic-1 Manhattan distance :")    
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_Astar_manhattan_distance(p);
        
    print("\nA* with heuristic-2 Euclidean distance :")  
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_Astar_Euclidean_distance(p);    
    
    print("\nA* with heuristic-3 Mispalced tiles :")      
    for j in list(range(len(input_matrix))):
        print ("\nsolution path",j+1,"for input (",input_matrix[j],"):")
        p = EightPuzzle()
        p.init_Matrix(input_matrix[j])
        search_Astar_Misplaced_tiles(p);  

    print ("\n===========================================")

    print ("Average Count: ")
    print ("BFS with heuristic-1 Manhattan distance: ", Final_Output[0][0]/5)
    print ("BFS with heuristic-2 Euclidean distance: ",Final_Output[0][1]/5)
    print ("BFS with heuristic-3 Misplaced tiles: ",    Final_Output[0][2]/5)
    print ("A* search with heuristic-1 Manhattan distance: ",  Final_Output[1][0]/5)
    print ("A* search with heuristic-2 Euclidean distance: ", Final_Output[1][1]/5)
    print ("A* search with heuristic-3 Misplaced tiles: ",     Final_Output[1][2]/5)
 
#Function to calculate path using BFS with Manhattan distance heuristic
def search_BFS_Manhattan_distance(p):
    path, count = p.BFS(h_manhattan_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[0][0] = Final_Output[0][0] +  len(path)
        print ("Solved with BFS with Manhattan distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")
        
#Function to calculate path using BFS with Euclidean distance heuristic
def search_BFS_Euclidean_distance(p):
    path, count = p.BFS(h_euclidean_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[0][1] = Final_Output[0][1] +  len(path)
        print ("Solved with BFS with Euclidean distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")
        
#Function to calculate path using BFS with Misplaced tiles heuristic
def search_BFS_Misplaced_tiles(p):
    path, count = p.BFS(h_misplaced_tiles)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[0][2] = Final_Output[0][2] +  len(path)
        print ("Solved with BFS & Misplaced tiles in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")

#Function to calculate path using Astar search with manhattan distance heuristic         
def search_Astar_manhattan_distance(p):        
    path, count = p.AstarSearch(h_manhattan_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[1][0] = Final_Output[1][0] +  len(path)
        print ("Solved with A* and Manhattan distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")

#Function to calculate path using Astar search with Euclidean distance heuristic
def search_Astar_Euclidean_distance(p):
    path, count = p.AstarSearch(h_euclidean_distance)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[1][1] = Final_Output[1][1] +  len(path)
        print ("Solved with A* and Euclidean distance in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")

#Function to calculate path using Astar search with Misplaced tiles heuristic
def search_Astar_Misplaced_tiles(p):
    path, count = p.AstarSearch(h_misplaced_tiles)
    if(path != []):
        path.reverse()
        for i in path:
            print (i.cloned_matrix)
        Final_Output[1][2] = Final_Output[1][2] +  len(path)
        print ("Solved with A* & Misplaced tiles in ", len(path) ,"steps exploring", count, "states")
    else:
        print ("Search aborted after exploring", count-1, "states")

if __name__ == "__main__":
    main()