import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QLineEdit,QTextEdit
from PyQt5.QtCore import pyqtSlot

import instLib

class Application (QMainWindow):
    def __init__(self):

        super().__init__()
        self.title = 'Inst_hashtag_statistic'
        self.left = 10
        self. top = 10
        self.wight = 300
        self.hight = 400
        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(10,10,400,400)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(20,30)
        self.textbox1.resize(360,40)

        self.textbox2 = QTextEdit(self)
        self.textbox2.move(20, 90)
        self.textbox2.resize(360, 200)

        self.button=QPushButton('View statistic',self)
        self.button.move(140,320)

        self.button.clicked.connect(self.on_click)

        self.show()






    @pyqtSlot()
    def on_click(self):

        strinput=self.textbox1.text()

        stringoutput="1"

        try:

            profile= instLib.Profile(strinput)
            stringoutput=strinput+'\n'
            stringoutput= "Число подписчиков: " + str(profile.countFollowers()) + "\n"

            try:
                stat = profile.getTagList()
                for i in sorted(stat.keys()):
                    stringoutput += i + ":" + str(stat[i]) + "\n"
            except:
                stringoutput="Аккаунт приватный"
        except:
            stringoutput="Аккаунта не существует"

        self.textbox2.setText(stringoutput)



app=QApplication(sys.argv)
wind=Application()
sys.exit(app.exec_())