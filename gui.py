import sys
from bot_rsi import BOT_RSI
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit, QFormLayout
from binance.enums import *

api_key = 'tutaj należy wpisać swój klucz api z binance'
api_secret = 'tutaj należy wpisać swój sekretny klucz api z binance'
para = "btcusdt"
interwal = "1m"
ile_kupujemy = 0.0005
rodzaj_zlecenia = ORDER_TYPE_MARKET
strona1, strona2 = SIDE_BUY, SIDE_SELL
rsi_z_ilu_swiec = 4
rsi_gora = 60
rsi_dol = 40


class Moje_Okno(QWidget):
    def __init__(self):
        super(Moje_Okno, self).__init__()
        self.setWindowTitle('Bot kryptowalutowy gui')
        self.setGeometry(100, 100, 280, 280)

        self.thread = {}
        self.przycisk_bot_rsi = QPushButton(self)
        self.przycisk_bot_rsi.setText("RSI BOT")
        self.przycisk_bot_rsi.clicked.connect(self.bot)
        self.przycisk_bot_rsi.move(5, 235)

        self.przycisk_zapisz = QPushButton(self)
        self.przycisk_zapisz.setText("Zapisz parametry")
        self.przycisk_zapisz.clicked.connect(self.zapisz)
        self.przycisk_zapisz.move(170, 170)

        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e3 = QLineEdit()
        self.e4 = QLineEdit()
        self.e5 = QLineEdit()
        self.e6 = QLineEdit()

        self.layout = QFormLayout()
        self.layout.addRow("Para:", self.e1)
        self.layout.addRow("Ile:", self.e2)
        self.layout.addRow("Jaki interwał:", self.e3)
        self.layout.addRow("Górna granica RSI:", self.e4)
        self.layout.addRow("Dolna granica RSI:", self.e5)
        self.layout.addRow("Z ilu świec RSI?:", self.e6)
        self.setLayout(self.layout)


    def zapisz(self):
        global para, para2, interwal, ile_kupujemy, rsi_z_ilu_swiec, rsi_dol, rsi_gora

        para = self.e1.text()
        para2 = para.upper()
        interwal = self.e3.text()
        ile_kupujemy = float(self.e2.text())
        rsi_z_ilu_swiec = int(self.e6.text())
        rsi_gora = int(self.e4.text())
        rsi_dol = int(self.e5.text())


    def bot(self):
        BOT_RSI.stworz_bota(api_key, api_secret, para, interwal, ile_kupujemy, rodzaj_zlecenia, strona1, strona2,
                            rsi_z_ilu_swiec, rsi_gora, rsi_dol)

def okno():
    app = QApplication(sys.argv)
    okno = Moje_Okno()
    okno.show()
    sys.exit(app.exec_())

okno()