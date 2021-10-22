"""a = {}
a["["+str(0)+","+str(0)+"]"] = [[0,1],[0,2]]
a["["+str(1)+","+str(0)+"]"] = [[1,1],[1,2]]

print(a["[0,0"])


for elem in self.constraint:
            for i in self.constraint[elem]:
                print(self.grid[i[0]][i[1]][0])"""
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLineEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QWidgetItem
from PySide6.QtGui import QPalette, QColor, QScreen, QGuiApplication, QFont
import PySide6
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku")
        
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
        for x in range(0,9):
            for y in range(0,9):
                box = QLineEdit()
                box.setMaxLength(1)
                font = box.font()
                font.setPointSize(30)
                box.setFont(font)
                box.setMaximumSize(40,40)
                box.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
                self.layout.addWidget(box, x, y)

        self.layout.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addLayout(self.layout)


        button = QPushButton("valider")
        button.clicked.connect(self.the_button_was_clicked)
        font = button.font()
        font.setPointSize(30)
        button.setFont(font)
        verticalLayout.addWidget(button)


        widget = QWidget()
        widget.setLayout(verticalLayout)
        self.setCentralWidget(widget)
        

        

    def the_button_was_clicked(self):
        layout = self.layout
        
        box = layout.itemAtPosition(0,0).widget()
        print(box.text())

        """for x in range(0,9):
            for y in range(0,9):
                box = layout.itemAtPosition(x,y).widget()
                print(box.text())"""
       



app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec_()