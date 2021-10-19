from random import randrange
import copy

class Map:
    def __init__(self):
        # la carte est sous forme de 5x5 cases, chacune est un vecteur [a,b,c] tel que a == 1 si contient Aspirateur ,b == 1 si saleté ,c == 1 si bijou 
        self.grid = [[[0] for i in range(9)] for j in range(9)]
        self.assignment = [[[0] for i in range(9)] for j in range(9)]
        self.domaine = [1, 2, 3, 4, 5, 6, 7, 8, 9]


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
        #Vérification des colonnes
        for i in range(0,9):
            liste1 = [1,2,3,4,5,6,7,8,9]
            liste2 = []
            for elem in self.assignment:
               liste2.append(elem[i][0])
            liste2.sort()
            if liste1!=liste2:
                return False

        #Vérification des lignes
        for column in self.assignment:
            liste1 = [1,2,3,4,5,6,7,8,9]
            liste2 = []
            for elem in column:
                liste2.append(elem[0])
            liste2.sort()
            if liste1!=liste2:
                return False

        #Vérification des cases
        liste1 = [1,2,3,4,5,6,7,8,9]
        liste2 = []
        for i in range(0,3):
            for j in range(0,3):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(0,3):
            for j in range(3,6):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(0,3):
            for j in range(6,9):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(0,3):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(3,6):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(6,9):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(0,3):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(3,6):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(6,9):
                liste2.append(self.assignment[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False
        
        return True


    def backtracking_search(self):
        print("backtracking_search")
        assignment = self.assignment
        return self.recursive_backtracking(assignment)


    def recursive_backtracking(self, assignment):
        print("recursive_search")
        if self.test_complete(assignment): return assignment
        x, y = self.select_unasigned_variable(assignment)

        for value in self.domaine:
            if self.test_consistant(assignment, x, y, value):
                assignment[x][y][0] = value
                result = self.recursive_backtracking(assignment)
                if result != False:
                    return result
                assignment[x][y][0] = 0
        return False
        

    def test_complete(self, assignment):
        complete = True
        for line in assignment:
            for box in line:
                if box[0] == 0:
                    complete = False
                    break
        return complete


    def select_unasigned_variable(self, assignment):
        #retourne les coordonnées d'une case vide
        #c'est dans cette partie que seront implémentés certains des 4 algorithmes
        return 0, 0


    def test_consistant(self, assignment, x, y, value):
        #test si la valeur est déjà présente dans la ligne ou dans la colonne
        for a in range(0,len(self.grid[0])):
            if ((self.grid[x][a][0] == value and a!=y) or (self.grid[a][y][0] == value and a != x)):
                return False

        #test si la valeur est déjà présente dans le bloc de cases
        col = x%3
        line = y%3
        combinations = []
        if col == 0 and line == 0:
            combinations.extend([[x+1,y+1],[x+1,y+2],[x+2,y+1],[x+2,y+2]])
        elif col == 0 and line == 1:
            combinations.extend([[x+1,y+1],[x+1,y-1],[x+2,y+1],[x+2,y-1]])
        elif col == 0 and line == 2:
            combinations.extend([[x+1,y-1],[x+1,y-2],[x+2,y-1],[x+2,y-2]])
        elif col == 1 and line == 0:
            combinations.extend([[x+1,y+1],[x+1,y+2],[x-1,y+1],[x-1,y+2]])
        elif col == 1 and line == 1:
            combinations.extend([[x+1,y+1],[x+1,y-1],[x-1,y+1],[x-1,y-1]])
        elif col == 1 and line == 2:
            combinations.extend([[x+1,y-1],[x+1,y-2],[x-1,y-1],[x-1,y-2]])
        elif col == 2 and line == 0:
            combinations.extend([[x-1,y+1],[x-1,y+2],[x-2,y+1],[x-2,y+2]])
        elif col == 2 and line == 1:
            combinations.extend([[x-1,y+1],[x-1,y-1],[x-2,y+1],[x-2,y-1]])
        elif col == 2 and line == 2:
            combinations.extend([[x-1,y-1],[x-1,y-2],[x-2,y-1],[x-2,y-2]])
        
        for [a, b] in combinations:
            if self.grid[a][b][0] == value:
                return False
        return True
            
    
    


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
   


    m.draw_map()
    m.grid = m.assignment
    m.backtracking_search()

    test = m.verif()
    print(test)

    print(9%3)


    