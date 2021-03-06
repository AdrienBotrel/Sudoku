from random import randrange
import copy
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLineEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QToolBar, QStatusBar, QWidgetItem, QColorDialog, QSpinBox
from PySide6.QtGui import QPalette, QColor, QScreen, QGuiApplication, QFont, QAction
import PySide6
import sys

import requests

USED_ALGO = "least constraining value"
#USED_ALGO = "mrv"
#USED_ALGO = "degree heuristic"
#USED_ALGO = "ac3"

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
        
        self.algo = USED_ALGO        
        print("> Used algorithme : ",self.algo)
    

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
        #print(self.assignment)
        if self.test_complete(): return self.assignment
        x, y = self.select_unasigned_variable()

        #Comme l'algorithme du least constraining value choisit les valeurs différement des autres algorithme,
        #on crée 3 boucles for pour s'adapter à la situation
        # Boucle du least constraining value
        if self.algo == "least constraining value":
            possible_values = self.leastConstrainingValue(x, y)
            for value,_ in possible_values:
                if self.test_consistant(x, y, value):
                    self.add(x,y,value)
                    result = self.recursive_backtracking()
                    if result != False:
                        return result
                    self.remove(x,y,value)
        
        # Boucle pour l'algorithme AC3
        elif self.algo == "ac3":
            for value in self.assignment[x][y][2]:
                
                #Add value
                prevVal=self.assignment[x][y][2]
                self.assignment[x][y][2]=[value]
                self.assignment[x][y][0] = value
                prevNb=self.assignment[x][y][1]
                self.assignment[x][y][1] = 1
                #Fin Add value

                self.AC3()
                
                result = self.recursive_backtracking()
                if result != False:
                    return result
                
                #Remove value
                self.assignment[x][y][0]=0           
                self.assignment[x][y][1]=prevNb
                self.assignment[x][y][2]=prevVal 
                self.update_legal_variable()
                #Fin Remove value

        #Boucle du MRV et du degree-heuristic       
        else:
            for value in self.assignment[x][y][2]:
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

        elif self.algo == "least constraining value" or self.algo=="ac3":
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

        if value in self.assignment[x][y][2]:
            return True
        
        return False


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
        self.assignment[x][y][2] = [value]
        self.assignment[x][y][1] = 1

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

        domainLocal = copy.copy(self.domain)
        for elem in list_constraint:
            if self.assignment[elem[0]][elem[1]][0] != 0 and  self.assignment[elem[0]][elem[1]][0] in domainLocal:
                domainLocal.remove(self.assignment[elem[0]][elem[1]][0])

        self.assignment[x][y][2] = domainLocal
        self.assignment[x][y][1] = len(domainLocal)

        for elem in list_constraint:
            if self.assignment[elem[0]][elem[1]][0] == 0:
                if value not in self.assignment[elem[0]][elem[1]][2]:
                    key_bis = "[" + str(elem[0]) + "," + str(elem[1]) + "]"
                    list_constraint_bis = self.constraint[key_bis]
                    add_value = True
                    for elem_bis in list_constraint_bis:
                        if value == self.assignment[elem_bis[0]][elem_bis[1]][0]:
                            add_value = False
                    if add_value:
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
    # Algorithme permettant de créer une liste de tous les arcs du sudoku 
    # (envisager de le créer une seule fois, self.all_arc=self.create_arc())
    def create_arc(self):
        var=self.constraint.copy()
        m_liste=[]
        for i in self.domain:
            for j in self.domain:
                key=[i-1,j-1]
                arc=var.pop('['+str(key[0])+','+str(key[1])+']')
                for k in arc:
                    m_liste+=[(key,k)]
        return m_liste
    
    # Algorithme testant si il existe au moins une valeur satisfaisant la contrainte (Xi,Xj)
    # Si il n'y a pas de y tel que x!=y, alors on renvoie True (la valeur x n'est pas consistente)
    def test_inconsistent_values(self,x,Xj):
        for y in self.assignment[Xj[0]][Xj[1]][2]:
            if x!=y:
                return False
        return True
    
    # Algorithme permettant d'enlever les valeurs x du domain de Xi si x n'est pas consistent
    # Renvoie True si au moins une valeur a été retiré, sinon renvoie False
    def remove_inconsistent_values(self,Xi,Xj):
        removed=False
        for x in self.assignment[Xi[0]][Xi[1]][2]:
            if self.test_inconsistent_values(x,Xj):
                self.assignment[Xi[0]][Xi[1]][2].remove(x)
                self.assignment[Xi[0]][Xi[1]][1]-=1
                removed=True
        return removed
    
    # Algorithme permettant d'actualiser les domaines des différentes cases en fonction des valeurs prises.
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
        self._createMenuBar() # créer une bare de menu
        self.length = 3
        
        self.init_screen()

    def init_screen(self):
        self.setWindowTitle("Sudoku")
        max_length = len(str(self.length*self.length))
        # print("max length : ",max_length)
        verticalLayout = QVBoxLayout()
        verticalLayout.setAlignment(PySide6.QtCore.Qt.AlignVCenter)

        self.text = QLabel()
        self.text.setText("Rentrez votre grille de sudoku puis appuyez sur \"Valider\"")
        font = self.text.font()
        font.setPointSize(30)
        self.text.setFont(font)
        self.text.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addWidget(self.text)


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


        validate_button = QPushButton("Valider")
        validate_button.clicked.connect(self.validate_button_clicked)
        font = validate_button.font()
        font.setPointSize(10)
        validate_button.setFont(font)

        verticalLayout.addWidget(validate_button)

        clear_button = QPushButton("Effacer")
        clear_button.clicked.connect(self.clear_button_clicked)
        font = clear_button.font()
        font.setPointSize(10)
        clear_button.setFont(font)

        verticalLayout.addWidget(clear_button)


        fill_button = QPushButton("* Remplir table Sudoku depuis Internet *")
        fill_button.clicked.connect(self.fill_button_clicked)
        font = fill_button.font()
        font.setPointSize(10)
        fill_button.setFont(font)

        verticalLayout.addWidget(fill_button)


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
            self.text.setText("Solution Trouvée")
        else:
            self.text.setText("Pas de solution")

        m.draw_map()


    #Retire toutes les valeurs du sudoku afin que l'utilisateur puisse rentrer un nouveau sudoku à résoudre
    def clear_button_clicked(self):
        layout = self.layout
        self.text.setText("Rentrez votre grille de sudoku puis appuyez sur \"Valider\"")
        for x in range(0,self.length*self.length):
            for y in range(0,self.length*self.length):
                box = layout.itemAtPosition(x,y).widget()
                box.setText("")
                box.setStyleSheet("color: black;")


    #Donner une valuer initiale à la table de sudoku à partir d'un site
    def fill_button_clicked(self):
        if self.length == 3:
            response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
            grid = response.json()['board']
            grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

            layout = self.layout
            m = Map(self.length)
            m.draw_map()

            #print(grid_original)

            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    box = layout.itemAtPosition(x,y).widget()
                    if grid_original[x][y]:
                        box.setStyleSheet("color: red;")
                        m.assignment[x][y][0] = int(grid_original[x][y])
                    else:
                        m.assignment[x][y][0] = 0

            for x in range(0,self.length*self.length):
                for y in range(0,self.length*self.length):
                    if (m.assignment[x][y][0] != 0):
                        box = layout.itemAtPosition(x,y).widget()
                        box.setText(str(m.assignment[x][y][0]))


    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        self.algoMenu = menuBar.addMenu("&Algorithme_utilisé")
        # algoMenu.addAction("alg1")
        # algoMenu.addAction("alg2")
        # algoMenu.addAction("alg3")
        # toolbar = QToolBar("My main toolbar")
        # self.addToolBar(toolbar)

        

        ac3_action = QAction("AC-3", self)
        ac3_action.setStatusTip("Algorithme AC-3")
        ac3_action.triggered.connect(self.onAC3ButtonClick)

        mrv_action = QAction("MRV", self)
        mrv_action.setStatusTip("Algorithme MRV")
        mrv_action.triggered.connect(self.onMRVButtonClick)

        degree_action = QAction("degree_heuristic", self)
        degree_action.setStatusTip("Algorithme degree heuristic")
        degree_action.triggered.connect(self.onDegreeHeuristicButtonClick)

        lcv_action = QAction("least_constraining_value", self)
        lcv_action.setStatusTip("Algorithme least constraining value")
        lcv_action.triggered.connect(self.onLeastConstrainingValueButtonClick)
        # toolbar.addAction(button_action)

        # self.setStatusBar(QStatusBar(self))
        self.algoMenu.addAction(ac3_action)
        self.algoMenu.addAction(mrv_action)
        self.algoMenu.addAction(degree_action)
        self.algoMenu.addAction(lcv_action)

        ####    Adding size variable
        editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        fontSizeSpinBox = QSpinBox()
        fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        editToolBar.addWidget(fontSizeSpinBox)
        fontSizeSpinBox.setMinimum(2)
        fontSizeSpinBox.setValue(3)
        fontSizeSpinBox.valueChanged.connect(self.value_changed)
        


    def value_changed(self, i):
        # Change the size of the Sudoku
        self.length = i
        print("Self.length : ",self.length)
        self.init_screen()

    def onAC3ButtonClick(self, s):
        global USED_ALGO
        USED_ALGO = "ac3"
        print(USED_ALGO)
        self.algoMenu.setTitle("&AC3")
        
    
    def onMRVButtonClick(self, s):
        global USED_ALGO
        USED_ALGO = "mrv"
        print(USED_ALGO)
        self.algoMenu.setTitle("&MRV")

    def onDegreeHeuristicButtonClick(self, s):
        global USED_ALGO
        USED_ALGO = "degree heuristic"
        print(USED_ALGO)
        self.algoMenu.setTitle("&degree heuristic")

    def onLeastConstrainingValueButtonClick(self, s):
        global USED_ALGO
        USED_ALGO = "least constraining value"
        print(USED_ALGO)   
        self.algoMenu.setTitle("&least constraining value")        



#Permet de lancer le code en affichant l'interface
if __name__ == "__main__":  

    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    app.exec()



    