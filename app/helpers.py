def calculateReturn(price, buy_price):
    percentage=(price-buy_price)/buy_price
    return round(percentage*100,2)
