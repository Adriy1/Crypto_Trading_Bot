import numpy as np
from botstrategy import BotStrategy

class stratRsi(BotStrategy):
    def __init__(self):
        super(stratRsi,self).__init__()
        self.zone = 0 # 0 : pas de zones, 1 : zone 1, 2 : zone 2, 3 : zone 3
        self.priceZ1 = 9999999999
        self.rsiZ1 = 100
        self.rsiZ2 = 0
        self.rsiZ3 = 100
        self.memory = 100
        self.countOpen = 0
        self.countClose = 0
        self.distanceMin = 15

    def condRsiOpen(self):
        rsi = self.indicators.RSI(self.prices)
        if self.countOpen > self.memory:
            self.resetOpen()
        if self.zone == 1:
            self.rsiZ1 = mini(rsi,self.rsiZ1)
            self.priceZ1 = mini(self.currentPrice,self.priceZ1) # on stocke le prix minimal
            if rsi > 35: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2
        elif self.zone == 2:
            self.rsiZ2 = maxi(rsi,self.rsiZ2) # on stocke le rsi de la zone 2

            if rsi < 30:
                if self.currentPrice < self.priceZ1 and rsi > self.rsiZ1 and self.countOpen >= self.distanceMin: # divergence : on passe en zone 3
                    self.zone = 3
                else:
                    self.resetOpen()
                    self.zone = 1
            if rsi > 65: # on reset si le rsi remonte trop
                self.resetOpen()
        elif self.zone == 3:
            self.rsiZ3 = min(rsi,self.rsiZ3)
            if rsi > self.rsiZ2: # achat
                self.resetOpen()
                return True
            elif self.rsiZ3 < self.rsiZ1:
                self.resetOpen()
                self.zone = 1
        else:
            if rsi < 30:
                self.resetOpen()
                self.zone = 1
        if self.zone != 0:
            self.countOpen += 1
        return False

    def condRsiClose(self):
        rsi = self.indicators.RSI(self.prices)
        if self.countClose > self.memory:
            self.resetClose()
        if self.zone == 1:
            self.rsiZ1 = maxi(rsi,self.rsiZ1)
            self.priceZ1 = maxi(self.currentPrice,self.priceZ1) # on stocke le prix maximal
            if rsi < 65: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2
        elif self.zone == 2:
            self.rsiZ2 = mini(rsi,self.rsiZ2) # on stocke le rsi de la zone 2
            if rsi > 70:
                if self.currentPrice > self.priceZ1 and rsi < self.rsiZ1 and self.countClose >= self.distanceMin: # divergence : on passe en zone 3
                    self.zone = 3
                else:
                    self.resetClose()
                    self.zone = 1
            if rsi < 40: # on reset si le rsi descend trop
                self.resetClose()
        elif self.zone == 3:
            self.rsiZ3 = maxi(rsi,self.rsiZ3)
            if rsi < self.rsiZ2: #on passe en zone 4
                self.resetClose()
                return True
            elif self.rsiZ3 > self.rsiZ1:
                self.resetOpen()
                self.zone = 1
        else:
            if rsi > 70:
                self.countClose = 0
                self.zone = 1
        if self.zone != 0:
            self.countClose += 1
        return False

    def resetOpen(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 0
        self.priceZ1 = 999999
        self.rsiZ1 = 100
        self.rsiZ3 = 100

    def resetClose(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 100
        self.priceZ1 = 0
        self.rsiZ1 = 0

    def conditionOpen(self,candlestick):
        # if candlestick.close > self.indicators.computeExpAverage(self.prices,candlestick,10) and candlestick.close > self.indicators.pointPivot(candlestick):
        if self.condRsiOpen():
            return True
        return False

    def conditionClose(self,candlestick,trade):
        # if candlestick.close < self.indicators.computeExpAverage(self.prices,candlestick,10) and candlestick.close < self.indicators.pointPivot(candlestick):
        #print("current price " + str(self.prices[-1]) + " on devrait vendre a "+str(pdv) + "(prix courant = " + str(trade.entryPrice) + ")")
        if self.condRsiClose():
			return True
        return False

def maxi(a,b):
    if a > b :
        return a
    else:
        return b

def mini(a,b):
    if a < b :
        return a
    else:
        return b
