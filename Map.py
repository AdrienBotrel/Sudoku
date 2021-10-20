from random import randrange
import copy
import time

class Map:
    def __init__(self):
        
        self.variables = [[[0] for i in range(9)] for j in range(9)]
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.constraint = {}
        
        self.assignment = [[[0, 0, []] for i in range(9)] for j in range(9)]

    
    def create_constraint(self):
        for x in range(0,9):
            for y in range(0,9):
                list_constraint = []
                #récupération des contraintes binaires
                for a in range(0,len(self.variables[0])):
                    if y!=a: list_constraint.append([x,a])
                    if x!=a: list_constraint.append([a,y])
                qx = int(x/3)
                qy = int(y/3)
                for i in range(0,3):
                    for j in range(0,3):
                        list_constraint.append([qx*3+i, qy*3+j])
                
                list_constraint.remove([x,y])
                new_list = []
                for l in list_constraint:
                    if l not in new_list: 
                        new_list.append(l)
                self.constraint["["+str(x)+","+str(y)+"]"] = new_list
        

    def draw_map(self):
        c = 0
        l=3
        
        for liste in self.assignment:
            if(l==3):
                print("  ", end = "")
                for i in range(0,13):
                    print(" - ", end = '')
                print("")
                l=0
            l+=1
            print(" || ", end = '')
            for elem in liste:
                c+=1
                if (elem[0] == 0):
                    print(" ", end = '')
                else:
                    print(elem[0], end = '')
                if (c==3):
                    print(" || ", end = '')
                    c=0
                else:
                    print(" | ", end = '')
            print("")
        
        print("  ", end = "")
        for i in range(0,13):
            print(" - ", end = '')
        print("")


    def verif(self):
        for x in range(0,9):
            for y in range(0,9):
                key = "[" + str(x) + "," + str(y) + "]"
                list_constraint = self.constraint[key]
                for elem in list_constraint:
                    if self.assignment[elem[0]][elem[1]][0] == self.assignment[x][y][0]:
                        return False
        
        return True


    def backtracking_search(self):
        return self.recursive_backtracking()


    def recursive_backtracking(self):
        if self.test_complete(): return self.assignment
        x, y = self.select_unasigned_variable()

        
        for value in self.domain:
            if self.test_consistant(x, y, value):
                self.add(x,y,value)
                result = self.recursive_backtracking()
                if result != False:
                    return result
                self.remove(x,y,value)
        return False
        
    #Vérifie si le sudoku est complet en analysant la valeur de chaque case
    def test_complete(self):
        complete = True
        for line in self.assignment:
            for box in line:
                if box[0] == 0:
                    complete = False
                    break
        return complete


    def select_unasigned_variable(self):
        #retourne les coordonnées d'une case vide
        #c'est dans cette partie que seront implémentés certains des 4 algorithmes

        #Algorithme MRV
        #selectedBox = [coord, legalValuesNumber]
        selectedBox = [[0,0], 10]
        for x in range(0,9):
            for y in range(0,9):
                if self.assignment[x][y][0] == 0:
                    if self.assignment[x][y][1] < selectedBox[1]:
                        selectedBox = [[x,y], self.assignment[x][y][1]]
        return selectedBox[0][0], selectedBox[0][1]
        
        """#Algorithme degree-heuristic
        #selectedBox = [coord, legalValuesNumber]
        selectedBox = [[10,10], 0]
        for x in range(0,9):
            for y in range(0,9):
                if self.assignment[x][y][0] == 0:
                    if self.assignment[x][y][1] > selectedBox[1]:
                        selectedBox = [[x,y], self.assignment[x][y][1]]
        return selectedBox[0][0], selectedBox[0][1]"""


    def test_consistant(self, x, y, value):
        if (x==10 and y ==10):
            return False

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if self.assignment[elem[0]][elem[1]][0] == value:
                return False
        return True


    def update_legal_variable(self):
        for x in range (0,9):
            for y in range (0,9):
                values = copy.copy(self.domain)

                key = "[" + str(x) + "," + str(y) + "]"
                list_constraint = self.constraint[key]
                for elem in list_constraint:
                    if self.assignment[elem[0]][elem[1]][0] in values:
                        values.remove(self.assignment[elem[0]][elem[1]][0])
                self.assignment[x][y][1] = len(values)
                self.assignment[x][y][2] = values


    def add(self, x, y, value):
        self.assignment[x][y][0] = value

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if value in self.assignment[elem[0]][elem[1]][2]:
                self.assignment[elem[0]][elem[1]][2].remove(value)
                self.assignment[elem[0]][elem[1]][1] -= 1
    

    def remove(self, x, y, value):
        self.assignment[x][y][0] = 0

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if value not in self.assignment[elem[0]][elem[1]][2]:
                self.assignment[elem[0]][elem[1]][2].append(value)
                self.assignment[elem[0]][elem[1]][1] += 1


if __name__ == "__main__":    
    m = Map()
    #for liste in m.grid:
    #    for elem in liste:
    #        elem[0] = randrange(0,10)
    #m.draw_map()

    """#Solution qui marche
    m.assignment[0][0][0] = 9
    m.assignment[0][1][0] = 3
    m.assignment[0][2][0] = 1
    m.assignment[0][3][0] = 8
    m.assignment[0][4][0] = 4
    m.assignment[0][5][0] = 2
    m.assignment[0][6][0] = 6
    m.assignment[0][7][0] = 7
    m.assignment[0][8][0] = 5

    m.assignment[1][0][0] = 4
    m.assignment[1][1][0] = 2
    m.assignment[1][2][0] = 5
    m.assignment[1][3][0] = 7
    m.assignment[1][4][0] = 3
    m.assignment[1][5][0] = 6
    m.assignment[1][6][0] = 9
    m.assignment[1][7][0] = 8
    m.assignment[1][8][0] = 1

    m.assignment[2][0][0] = 8
    m.assignment[2][1][0] = 6
    m.assignment[2][2][0] = 7
    m.assignment[2][3][0] = 1
    m.assignment[2][4][0] = 5
    m.assignment[2][5][0] = 9
    m.assignment[2][6][0] = 4
    m.assignment[2][7][0] = 2
    m.assignment[2][8][0] = 3

    m.assignment[3][0][0] = 6
    m.assignment[3][1][0] = 8
    m.assignment[3][2][0] = 4
    m.assignment[3][3][0] = 2
    m.assignment[3][4][0] = 1
    m.assignment[3][5][0] = 3
    m.assignment[3][6][0] = 7
    m.assignment[3][7][0] = 5
    m.assignment[3][8][0] = 9

    m.assignment[4][0][0] = 5
    m.assignment[4][1][0] = 9
    m.assignment[4][2][0] = 2
    m.assignment[4][3][0] = 6
    m.assignment[4][4][0] = 7
    m.assignment[4][5][0] = 8
    m.assignment[4][6][0] = 1
    m.assignment[4][7][0] = 3
    m.assignment[4][8][0] = 4

    m.assignment[5][0][0] = 1
    m.assignment[5][1][0] = 7
    m.assignment[5][2][0] = 3
    m.assignment[5][3][0] = 5
    m.assignment[5][4][0] = 9
    m.assignment[5][5][0] = 4
    m.assignment[5][6][0] = 8
    m.assignment[5][7][0] = 6
    m.assignment[5][8][0] = 2

    m.assignment[6][0][0] = 2
    m.assignment[6][1][0] = 5
    m.assignment[6][2][0] = 9
    m.assignment[6][3][0] = 4
    m.assignment[6][4][0] = 8
    m.assignment[6][5][0] = 7
    m.assignment[6][6][0] = 3
    m.assignment[6][7][0] = 1
    m.assignment[6][8][0] = 6

    m.assignment[7][0][0] = 3
    m.assignment[7][1][0] = 1
    m.assignment[7][2][0] = 8
    m.assignment[7][3][0] = 9
    m.assignment[7][4][0] = 6
    m.assignment[7][5][0] = 5
    m.assignment[7][6][0] = 2
    m.assignment[7][7][0] = 4
    m.assignment[7][8][0] = 7

    m.assignment[8][0][0] = 7
    m.assignment[8][1][0] = 4
    m.assignment[8][2][0] = 6
    m.assignment[8][3][0] = 3
    m.assignment[8][4][0] = 2
    m.assignment[8][5][0] = 1
    m.assignment[8][6][0] = 5
    m.assignment[8][7][0] = 9
    m.assignment[8][8][0] = 8"""


    #Solution à tester
    m.assignment[0][2][0] = 1
    m.assignment[0][3][0] = 8
    m.assignment[0][5][0] = 2
    m.assignment[0][6][0] = 6
    m.assignment[0][7][0] = 7

    m.assignment[1][0][0] = 4
    m.assignment[1][2][0] = 5

    m.assignment[2][0][0] = 8
    m.assignment[2][1][0] = 6
    m.assignment[2][5][0] = 9
    m.assignment[2][7][0] = 2
    m.assignment[2][8][0] = 3

    m.assignment[3][2][0] = 4
    m.assignment[3][4][0] = 1
    m.assignment[3][6][0] = 7
    m.assignment[3][8][0] = 9

    m.assignment[4][0][0] = 5
    m.assignment[4][1][0] = 9
    m.assignment[4][2][0] = 2
    m.assignment[4][4][0] = 7
    m.assignment[4][8][0] = 4

    m.assignment[5][2][0] = 3
    m.assignment[5][3][0] = 5
    m.assignment[5][7][0] = 6
    m.assignment[5][8][0] = 2

    m.assignment[6][2][0] = 9
    m.assignment[6][4][0] = 8
    m.assignment[6][5][0] = 7
    m.assignment[6][6][0] = 3
    m.assignment[6][8][0] = 6

    m.assignment[7][1][0] = 1
    m.assignment[7][7][0] = 4

    m.assignment[8][3][0] = 3
    m.assignment[8][4][0] = 2
    m.assignment[8][5][0] = 1
    m.assignment[8][6][0] = 5
    m.assignment[8][8][0] = 8
   

    m.create_constraint()
    m.update_legal_variable()
    m.draw_map()
    m.grid = m.assignment
    m.backtracking_search()
    m.draw_map()
    test = m.verif()
    print(test)
    print(m.assignment)



    