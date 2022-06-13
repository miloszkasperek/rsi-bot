import websocket, json
import numpy as np
import talib
from binance.client import Client


class BOT_RSI():
    def __init__(self, api_key, api_secret, para, interwal, ile_kupujemy, rodzaj_zlecenia, strona1, strona2, rsi_z_ilu_swiec, rsi_gora, rsi_dol):
        self.api_key = api_key
        self.api_secret = api_secret
        self.para = para
        self.para2 = self.para.upper()
        self.interwal = interwal
        self.ile_kupujemy = ile_kupujemy
        self.rodzaj_zlecenia = rodzaj_zlecenia
        self.socket = f"wss://stream.binance.com:9443/ws/{self.para}@kline_{self.interwal}"
        self.ceny_koncowe_swiec = []
        self.client = Client(self.api_key, self.api_secret)
        self.strona1 = strona1
        self.strona2 = strona2
        self.rsi_z_ilu_swiec = rsi_z_ilu_swiec

        self.rsi_gora = rsi_gora
        self.rsi_dol = rsi_dol
        self.czy_w_pozycji = False
        self.liczba_swiec = 0
        self.uruchom_bota()

    def kup(self, co, ile, rodzaj):
        zlecenie = self.client.create_order(symbol = co, quantity = ile, type = rodzaj, side = self.strona1)
        print(zlecenie)


    def sprzedaj(self, co, ile, rodzaj):
        zlecenie = self.client.create_order(symbol = co, quantity = ile, type = rodzaj, side = self.strona2)
        print(zlecenie)



    def on_open(self, ws):
        print("STARTUJEMY...")


    def on_error(self, ws, error):
        print(error)

    def on_message(self, ws, message):

        json_message = json.loads(message)
        swieca = json_message['k']


        czy_koniec_swiecy = swieca['x']
        cena_koncowa = swieca['c']
        if czy_koniec_swiecy:
            self.liczba_swiec += 1
            print(f"Świeca numer: {self.liczba_swiec}")
            print("Czy w pozycji: ", self.czy_w_pozycji)
            self.ceny_koncowe_swiec.append(float(cena_koncowa))
            if self.liczba_swiec > self.rsi_z_ilu_swiec:
                ceny_numpy = np.array(self.ceny_koncowe_swiec)
                lista_rsi = talib.RSI(ceny_numpy, self.rsi_z_ilu_swiec)
                ostatnie_rsi = lista_rsi[-1]
                print("Ostatnie RSI: ", ostatnie_rsi)
                if ostatnie_rsi < self.rsi_dol and not self.czy_w_pozycji:
                    print("Kupuję.")
                    self.kup(self.para2, self.ile_kupujemy, self.rodzaj_zlecenia)
                    self.czy_w_pozycji = True
                elif ostatnie_rsi > self.rsi_gora and self.czy_w_pozycji:
                    print('Sprzedaję.')
                    self.sprzedaj(self.para2, self.ile_kupujemy, self.rodzaj_zlecenia)
                    self.czy_w_pozycji = False

                else: print("Ani nie kupuję, ani nie sprzedaję.")



    def uruchom_bota(self):
        ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_error=self.on_error, on_message=self.on_message)
        print(self.socket)
        ws.run_forever()

    @staticmethod
    def stworz_bota(api_key, api_secret, para, interwal, ile_kupujemy, rodzaj_zlecenia, strona1, strona2, rsi_z_ilu_swiec, rsi_gora, rsi_dol):
        bocik = BOT_RSI(api_key, api_secret, para, interwal, ile_kupujemy, rodzaj_zlecenia, strona1, strona2, rsi_z_ilu_swiec, rsi_gora, rsi_dol)





