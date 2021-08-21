import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


# temp example gui
class WildfireGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Wildfire Simulator'
        self.left = 500
        self.top = 300
        self.width = 500
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WildfireGUI()
    sys.exit(app.exec_())