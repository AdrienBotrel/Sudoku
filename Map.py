from random import randrange

class Map:
    def __init__(self):
        # la carte est sous forme de 5x5 cases, chacune est un vecteur [a,b,c] tel que a == 1 si contient Aspirateur ,b == 1 si saleté ,c == 1 si bijou 
        self.grid = [[[0] for i in range(9)] for j in range(9)]

    def draw_map(self):
        c = 0
        l=3
        
        for liste in self.grid:
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
            for elem in self.grid:
               liste2.append(elem[i][0])
            liste2.sort()
            if liste1!=liste2:
                return False

        #Vérification des lignes
        for column in self.grid:
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
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(0,3):
            for j in range(3,6):
                print(list)
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(0,3):
            for j in range(6,9):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(0,3):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(3,6):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(3,6):
            for j in range(6,9):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(0,3):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(3,6):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False

        liste2 = []
        for i in range(6,9):
            for j in range(6,9):
                liste2.append(self.grid[i][j][0])
        liste2.sort()
        if liste1!=liste2:
            return False
        
        return True


if __name__ == "__main__":    
    m = Map()
    #for liste in m.grid:
    #    for elem in liste:
    #        elem[0] = randrange(0,10)
    #m.draw_map()

    #Solution qui marche
    m.grid[0][0][0] = 9
    m.grid[0][1][0] = 3
    m.grid[0][2][0] = 1
    m.grid[0][3][0] = 8
    m.grid[0][4][0] = 4
    m.grid[0][5][0] = 2
    m.grid[0][6][0] = 6
    m.grid[0][7][0] = 7
    m.grid[0][8][0] = 5

    m.grid[1][0][0] = 4
    m.grid[1][1][0] = 2
    m.grid[1][2][0] = 5
    m.grid[1][3][0] = 7
    m.grid[1][4][0] = 3
    m.grid[1][5][0] = 6
    m.grid[1][6][0] = 9
    m.grid[1][7][0] = 8
    m.grid[1][8][0] = 1

    m.grid[2][0][0] = 8
    m.grid[2][1][0] = 6
    m.grid[2][2][0] = 7
    m.grid[2][3][0] = 1
    m.grid[2][4][0] = 5
    m.grid[2][5][0] = 9
    m.grid[2][6][0] = 4
    m.grid[2][7][0] = 2
    m.grid[2][8][0] = 3

    m.grid[3][0][0] = 6
    m.grid[3][1][0] = 8
    m.grid[3][2][0] = 4
    m.grid[3][3][0] = 2
    m.grid[3][4][0] = 1
    m.grid[3][5][0] = 3
    m.grid[3][6][0] = 7
    m.grid[3][7][0] = 5
    m.grid[3][8][0] = 9

    m.grid[4][0][0] = 5
    m.grid[4][1][0] = 9
    m.grid[4][2][0] = 2
    m.grid[4][3][0] = 6
    m.grid[4][4][0] = 7
    m.grid[4][5][0] = 8
    m.grid[4][6][0] = 1
    m.grid[4][7][0] = 3
    m.grid[4][8][0] = 4

    m.grid[5][0][0] = 1
    m.grid[5][1][0] = 7
    m.grid[5][2][0] = 3
    m.grid[5][3][0] = 5
    m.grid[5][4][0] = 9
    m.grid[5][5][0] = 4
    m.grid[5][6][0] = 8
    m.grid[5][7][0] = 6
    m.grid[5][8][0] = 2

    m.grid[6][0][0] = 2
    m.grid[6][1][0] = 5
    m.grid[6][2][0] = 9
    m.grid[6][3][0] = 4
    m.grid[6][4][0] = 8
    m.grid[6][5][0] = 7
    m.grid[6][6][0] = 3
    m.grid[6][7][0] = 1
    m.grid[6][8][0] = 6

    m.grid[7][0][0] = 3
    m.grid[7][1][0] = 1
    m.grid[7][2][0] = 8
    m.grid[7][3][0] = 9
    m.grid[7][4][0] = 6
    m.grid[7][5][0] = 5
    m.grid[7][6][0] = 2
    m.grid[7][7][0] = 4
    m.grid[7][8][0] = 7

    m.grid[8][0][0] = 7
    m.grid[8][1][0] = 4
    m.grid[8][2][0] = 6
    m.grid[8][3][0] = 3
    m.grid[8][4][0] = 2
    m.grid[8][5][0] = 1
    m.grid[8][6][0] = 5
    m.grid[8][7][0] = 9
    m.grid[8][8][0] = 8

   
    m.draw_map()
    test = m.verif()
    print(test)