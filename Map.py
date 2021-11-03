from random import randrange
import copy
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLineEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QWidgetItem, QColorDialog
from PySide6.QtGui import QPalette, QColor, QScreen, QGuiApplication, QFont
import PySide6
import sys

class Map:
    def __init__(self, length):
        #taille de la grille (3 correspond à une grille de 9*9)
        self.length = length

        #Modélisation du CSP avec définition de VDC (Variable, domaine, contraintes)
        self.variables = [[[0] for i in range(length*length)] for j in range(length*length)]
        self.domain = []
        for l in range(1, length*length + 1):
            self.domain.append(l)
        self.constraint = {}
        
        #Définition de l'assignement avec une grille de 9*9
        #Chaque case est défini par sa valeur, le nombre de valeur disponible et la liste des valeurs disponibles
        self.assignment = [[[0, 0, []] for i in range(length*length)] for j in range(length*length)]
        #Pour le moment, l'algorithme utilisé est défini ici
        #self.algo = "mrv"
        #self.algo = "degree heuristic"
        self.algo = "least constraining value"

    
    #Créer un dictionnaire avec pour clé les coordonnées des cases de la grille et en valeur
    #les coordonnées de toutes les cases possédant des contraintes binaires avec la case en clé
    def create_constraint(self):
        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                list_constraint = []
                #récupération des contraintes binaires
                for a in range(0,len(self.variables[0])):
                    if y!=a: list_constraint.append([x,a])
                    if x!=a: list_constraint.append([a,y])
                qx = int(x/self.length)
                qy = int(y/self.length)
                for i in range(0,self.length):
                    for j in range(0,self.length):
                        list_constraint.append([qx*self.length+i, qy*self.length+j])
                
                list_constraint.remove([x,y])
                new_list = []
                for l in list_constraint:
                    if l not in new_list: 
                        new_list.append(l)
                self.constraint["["+str(x)+","+str(y)+"]"] = new_list


    #Utilisé pour afficher le sudoku dans le terminal
    #Surtout utilisé au départ dans la phase de test
    def draw_map(self):
        c = 0
        l= self.length
        
        for liste in self.assignment:
            if(l==self.length):
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
                if (c==self.length):
                    print(" || ", end = '')
                    c=0
                else:
                    print(" | ", end = '')
            print("")
        
        print("  ", end = "")
        for i in range(0,self.length*self.length+4):
            print(" - ", end = '')
        print("")


    #Utilisé pour vérifier que les conditions du sudoku sont respectées
    #On compare la valeur de chaque case avec les valeurs des cases avec des contraintes associées
    def verif(self):
        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                key = "[" + str(x) + "," + str(y) + "]"
                list_constraint = self.constraint[key]
                for elem in list_constraint:
                    if self.assignment[elem[0]][elem[1]][0] == self.assignment[x][y][0]:
                        return False
        
        return True


    #Permet de lancer la boucle du backtracking (comme dans le pseudo code)
    def backtracking_search(self):
        return self.recursive_backtracking()


    #Boucle de backtracking (comme dans le pseudo code)
    def recursive_backtracking(self):
        print(self.assignment)
        if self.test_complete(): return self.assignment
        x, y = self.select_unasigned_variable()
        #Comme l'algorithme du least constraining value choisit les valeurs différement des autres algorithme,
        #on crée 2 boucles for pour s'adapter à la situation
        if self.algo == "least constraining value":
            possible_values = self.leastConstrainingValue(x, y)
            for value,_ in possible_values:
                if self.test_consistant(x, y, value):
                    self.add(x,y,value)
                    result = self.recursive_backtracking()
                    if result != False:
                        return result
                    self.remove(x,y,value)
        else:
            for value in self.domain:
                if self.test_consistant(x, y, value):
                    self.add(x,y,value)
                    result = self.recursive_backtracking()
                    if result != False:
                        return result
                    self.remove(x,y,value)
        return False
        

    #Vérifie si le sudoku est complet en analysant la valeur de chaque case
    #Tant qu'une case est toujours égale à zéro (pas attribué), on continue la boucle de backtracking 
    def test_complete(self):
        complete = True
        for line in self.assignment:
            for box in line:
                if box[0] == 0:
                    complete = False
                    break
        return complete


    #retourne les coordonnées d'une case vide
    #c'est dans cette partie que seront implémentés le MRV et le degree heuristic
    def select_unasigned_variable(self):
        if self.algo == "mrv":
            #Algorithme MRV
            #selectedBox = [coord, legalValuesNumber]
            selectedBox = [[0,0], self.length*self.length + 1]
            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    if self.assignment[x][y][0] == 0:
                        if self.assignment[x][y][1] < selectedBox[1]:
                            selectedBox = [[x,y], self.assignment[x][y][1]]
        elif self.algo == "degree heuristic": 
            #Algorithme degree-heuristic
            #selectedBox = [coord, legalValuesNumber]
            selectedBox = [[self.length*self.length+1,self.length*self.length+1], 0]
            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    if self.assignment[x][y][0] == 0:
                        key = "[" + str(x) + "," + str(y) + "]"
                        if len(self.constraint[key]) > selectedBox[1]:
                            selectedBox = [[x,y], self.assignment[x][y][1]]

        elif self.algo == "least constraining value":
            #Algorithme de least constraining value
            #selectBox = [coord, legalValuesNumber]
            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    if self.assignment[x][y][0] == 0:
                        selectedBox = [[x,y], self.assignment[x][y][1]]
                        return selectedBox[0][0], selectedBox[0][1]

        return selectedBox[0][0], selectedBox[0][1]

    
    #On test si la valeur donnée en paramètres est déjà utilisée dans les cases possédant des
    #contraintes binaires avec la case[x,y]. Si c'est le cas, on passe à la contrainte suivante
    def test_consistant(self, x, y, value):
        if (x==self.length*self.length+1 and y==self.length*self.length+1):
            return False

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if self.assignment[elem[0]][elem[1]][0] == value:
                return False
        return True


    #On initialise la variable assignment avec les valeurs déjà définies par l'utilisateur
    #A modifier pour les contraintes
    def update_legal_variable(self):
        for x in range (0,self.length*self.length):
            for y in range (0,self.length*self.length):
                values = copy.copy(self.domain)

                if self.assignment[x][y][0] != 0:
                    self.assignment[x][y][1] = 1
                    self.assignment[x][y][2] = [self.assignment[x][y][0]]
                else :
                    key = "[" + str(x) + "," + str(y) + "]"
                    list_constraint = self.constraint[key]
                    for elem in list_constraint:
                        if self.assignment[elem[0]][elem[1]][0] in values:
                            values.remove(self.assignment[elem[0]][elem[1]][0])
                    
                    self.assignment[x][y][1] = len(values)
                    self.assignment[x][y][2] = values


    #Ajoute une valeur à une case dans la variable assignment. 
    #On modifie les valeurs possibles pour les cases avec des contraintes binaires 
    def add(self, x, y, value):
        self.assignment[x][y][0] = value

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if value in self.assignment[elem[0]][elem[1]][2]:
                self.assignment[elem[0]][elem[1]][2].remove(value)
                self.assignment[elem[0]][elem[1]][1] -= 1
    

    #Retire une valeur à une case dans la variable assignment. 
    #On modifie les valeurs possibles pour les cases avec des contraintes binaires 
    def remove(self, x, y, value):
        self.assignment[x][y][0] = 0

        key = "[" + str(x) + "," + str(y) + "]"
        list_constraint = self.constraint[key]

        for elem in list_constraint:
            if value not in self.assignment[elem[0]][elem[1]][2]:
                self.assignment[elem[0]][elem[1]][2].append(value)
                self.assignment[elem[0]][elem[1]][1] += 1


    #Algorithme permettant de récupérer la liste des valeurs possibles pour l'algorithme de least constraining value
    #Les valeurs sot triés de celle modifiant le moins les valeurs possibles pour les cases avec des contraintes binaires
    # jusque celle les modifiant le plus 
    def leastConstrainingValue(self, x, y):
        values = []
        for v in self.domain:
            values.append([v, 0])
        constraint = self.constraint["["+str(x)+","+str(y)+"]"]

        for v in values:
            n = 0
            for c in constraint:
                if self.assignment[c[0]][c[1]][0]==0 and v[0] in self.assignment[c[0]][c[1]][2]:
                    n += 1
            v[1] = n
        
        values.sort(key = lambda x: x[1])
        return values




    ## AC3
    
    def create_arc(self):
        var=self.constraint.copy()
        m_liste=[]
        for i in self.domain:
            for j in self.domain:
                key=[i-1,j-1]
                arc=var.pop('['+str(key[0])+','+str(key[1])+']')
                for k in arc:
                    if (k,key) not in m_liste:
                        m_liste+=[(key,k)]
        return m_liste
    
    def test_inconsistent_values(self,x,Xj):
        for y in self.assignment[Xj[0]][Xj[1]][2]:
            if x!=y:
                return False
        return True
    
    def remove_inconsistent_values(self,Xi,Xj):
        removed=False
        for x in self.assignment[Xi[0]][Xi[1]][2]:
            if self.test_inconsistent_values(x,Xj):
                self.assignment[Xi[0]][Xi[1]][2].remove(x)
                self.assignment[Xi[0]][Xi[1]][1]-=1
                removed=True
        return removed
    
    def AC3(self):
        queue=self.create_arc()
        while(len(queue)>0):
            Xi, Xj=queue.pop(0)
            if self.remove_inconsistent_values(Xi,Xj):
                for Xk in self.constraint.get('['+str(Xi[0])+','+str(Xi[1])+']'):
                    queue+=[(Xk,Xi)]


        
#classe s'occupant de l'affichage du sudoku dans une fenêtre à part
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.length = 2
        self.setWindowTitle("Sudoku")
        max_length = len(str(self.length*self.length))
        print(max_length)
        verticalLayout = QVBoxLayout()
        verticalLayout.setAlignment(PySide6.QtCore.Qt.AlignVCenter)

        text = QLabel()
        text.setText("Rentrez votre grille de sudoku puis appuyez sur \"Valider\"")
        font = text.font()
        font.setPointSize(30)
        text.setFont(font)
        text.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addWidget(text)


        self.layout = QGridLayout()
        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                box = QLineEdit()
                box.setMaxLength(max_length)
                font = box.font()
                font.setPointSize(100/self.length)
                box.setFont(font)
                box.setMaximumSize(150/self.length,150/self.length)
                box.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
                self.layout.addWidget(box, x, y)

        self.layout.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addLayout(self.layout)


        validate_button = QPushButton("valider")
        validate_button.clicked.connect(self.validate_button_clicked)
        font = validate_button.font()
        font.setPointSize(30)
        validate_button.setFont(font)

        verticalLayout.addWidget(validate_button)

        clear_button = QPushButton("effacer")
        clear_button.clicked.connect(self.clear_button_clicked)
        font = clear_button.font()
        font.setPointSize(30)
        clear_button.setFont(font)

        verticalLayout.addWidget(clear_button)


        widget = QWidget()
        widget.setLayout(verticalLayout)
        self.setCentralWidget(widget)
        

    #Récupère les valeurs données par l'utilisateur, utilise le backtracking pour résoudre le sudoku 
    # et affiche le résultat obtenu
    def validate_button_clicked(self):
        layout = self.layout
        m = Map(self.length)
        m.draw_map()

        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                box = layout.itemAtPosition(x,y).widget()
                if box.text() == "":
                    m.assignment[x][y][0] = 0
                else:
                    box.setStyleSheet("color: red;")
                    m.assignment[x][y][0] = int(box.text())
        m.draw_map()
        m.create_constraint()
        m.update_legal_variable()
        m.grid = m.assignment
        if(m.backtracking_search()!=False):
            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    box = layout.itemAtPosition(x,y).widget()
                    box.setText(str(m.assignment[x][y][0]))

        m.draw_map()


    #Retire toutes les valeurs du sudoku afin que l'utilisateur puisse rentrer un nouveau sudoku à résoudre
    def clear_button_clicked(self):
        layout = self.layout

        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                box = layout.itemAtPosition(x,y).widget()
                box.setText("")
                box.setStyleSheet("color: black;")

                



#Permet de lancer le code en affichant l'interface
if __name__ == "__main__":    
    """m = Map()
    #for liste in m.grid:
    #    for elem in liste:
    #        elem[0] = randrange(0,10)
    #m.draw_map()

    #Solution qui marche
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
    m.assignment[8][8][0] = 8


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
    print(m.assignment)"""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    app.exec_()



    