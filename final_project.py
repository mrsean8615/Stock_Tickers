import requests
import json
import time

tickers = ['AAPL', 'ADBE', 'DE', 'F', 'GM', 'GOOG', 'MSFT', 'NKE', 'NVDA', 'PEP']

def create_data(tickers):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey=YKC3EUDUOOQG2IBW'
    r = requests.get(url)
    data = json.loads(r.text)
    time.sleep(12)
    
    time_key = 'Time Series (Daily)'
    adj_close_key = '5. adjusted close'
    
    csv_file = open(f"/home/ubuntu/environment/final_project/data/{ticker}.csv", 'w')
    
    lst = []
    for date in data[time_key]:
        # print(ticker, date, data[time_key][date][adj_close_key])
        lst.append(ticker + "," + date + "," + data[time_key][date][adj_close_key] + "\n")
    rev_lst = lst[0:260]
    rev_lst.reverse()
    
    for l in rev_lst:
        csv_file.write(l)
    csv_file.close()
    return rev_lst
        

def read_data(ticker):
    prices = []
    with open(f'/home/ubuntu/environment/final_project/data/{ticker}.csv') as data:
        for row in data:
            ticker, date, adj_close = row.split(",")
            prices.append(float(adj_close.replace('\n', "")))
            
    return ticker, prices

def meanReversionStrategy(prices, ticker):
    i = 0
    buy = 0
    profit = 0
    firstBuy = 0
    sell = 0
    position = 0

    print(f"{ticker} Mean Reversion Strategy Output:")
    for price in prices:
        if i >= 5:
            avg = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
            
            #Buying logic
            if price < avg * 0.98 and position != 1:
               print(f"buy at: {round(price,2)}")
               buy = round(price, 2)
               profit += sell - buy
               print(f'trade profit: {round(price - buy, 2)}')
               if price == prices[-1]:
                   print("You should buy this stock today!")
               if firstBuy == 0:
                   firstBuy = round(price,2)
               position = 1
            #Selling Logic
            elif price > avg * 1.02 and position != -1:
                sell = round(price, 2)
                print(f"sell at: {round(price,2)}")
                print(f"trade profit: {round(price - buy, 2)}")
                if price == prices[-1]:
                    print("You should sell this stock today!")
                profit += sell - buy
                buy = 0
                position = -1
            else:
                pass
        i += 1
    
    returnPercent = f"{round((profit / firstBuy) * 100, 2)}%"
    
    output(profit, firstBuy, returnPercent)
    return round(profit, 2), returnPercent

def simpleMovingAverageStrategy(prices, ticker):
    i = 0
    buy = 0
    profit = 0
    firstBuy = 0
    sell = 0
    position = 0

    
    print(f"{ticker} Simple Moving Average Strategy Output:")
    for price in prices:
        if i >= 5:
            avg = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
            
            #Buying logic
            if price > avg and position != 1:
                print(f"buy at: {round(price,2)}")
                buy = round(price, 2)
                profit += sell - buy
                print(f'trade profit: {round(price - buy, 2)}')
                if price == prices[-1]:
                    print("You should buy this stock today!")
                if firstBuy == 0:
                    firstBuy = round(price,2)
                position = 1
                   
            #Selling Logic
            elif price < avg and position != -1:
                sell = round(price, 2)
                print(f"sell at: {round(price,2)}")
                print(f"trade profit: {round(price - buy, 2)}")
                if price == prices[-1]:
                    print("You should sell this stock today!")
                profit += sell - buy
                buy = 0
                position = -1
            else:
                pass
        i += 1
        
    returnPercent = f"{round((profit / firstBuy) * 100, 2)}%"
    
    output(profit, firstBuy, returnPercent)
    
    return round(profit, 2), returnPercent
    
def bollingerMethod(prices, ticker):
    i = 0
    buy = 0
    profit = 0
    firstBuy = 0
    sell = 0
    position = 0
    
    print(f"{ticker} Bollinger Method Output:")
    for price in prices:
        if i >= 5:
            avg = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5
            
            #Buying logic
            if price > avg *1.05 and position != 1:
                print(f"buy at: {round(price,2)}")
                buy = round(price, 2)
                profit += sell - buy
                print(f'trade profit: {round(price - buy, 2)}')
                if price == prices[-1]:
                    print("You should buy this stock today!")
                if firstBuy == 0:
                   firstBuy = round(price,2)
                position = 1
                   
            #Selling Logic
            elif price < avg *.95 and position != -1:
                sell = round(price, 2)
                print(f"sell at: {round(price,2)}")
                print(f"trade profit: {round(price - buy, 2)}")
                if price == prices[-1]:
                    print("You should sell this stock today!")
                profit += sell - buy
                buy = 0
                position = -1
            else:
                pass
        i += 1
        
    returnPercent = f"{round((profit / firstBuy) * 100, 2)}%"
    
    output(profit, firstBuy, returnPercent)


    return round(profit, 2), returnPercent
    
#Outputting to JSON
def saveResults(result): 
    json.dump(dictionary, open(f'/home/ubuntu/environment/final_project/results.json', "w"), indent=4)

def output(profit, firstBuy, returnPercent):
    #Output
    print('-------------')
    print(f'Total Profit: {round(profit, 2)}')
    print(f'First Buy: {firstBuy}')
    print(f'Percentage Return%: {returnPercent}', end='\n\n')


dictionary = {}
meanProfits = {}
simpleProfits = {}
bProfits = {}

#Going through all stocks in the tickers list
for ticker in tickers:
    #read from file
    prices = create_data(tickers)  
    title, data = read_data(ticker)
    
    dictionary[f"{ticker}_prices"] = prices

    #Mean Reversion Returns
    meanProfit, meanReturn = meanReversionStrategy(data, ticker) 
    dictionary[ticker + "_mr_profit"] = meanProfit
    meanProfits[ticker] = meanProfit	
    dictionary[ticker + "_mr_returns"] = meanReturn

    #Simple Moving Average
    simpleProfit, simpleReturn = simpleMovingAverageStrategy(data, ticker)
    dictionary[ticker + "_sma_profit"] = simpleProfit
    simpleProfits[ticker] = simpleProfit	
    dictionary[ticker + "_sma_returns"] = simpleReturn
    
    #bollinger Method
    bProfit, bReturn = bollingerMethod(data, ticker)
    dictionary[ticker + "_b_profit"] = bProfit
    bProfits[ticker] = bProfit	
    dictionary[ticker + "_b_returns"] = bReturn
    
#Gets top stocks for mean reversion
sorted_mean_profits = sorted(meanProfits.items(), key=lambda x: x[1], reverse=True)
print("Best Stocks with Mean Reversion")
for i in sorted_mean_profits:
	print(i[0], "-->", i[1])
print('\n')

#Gets top stocks for simple moving average 
sorted_simple_profits = sorted(simpleProfits.items(), key=lambda x: x[1], reverse=True)
print("Best Stocks with Simple Moving Average")
for i in sorted_simple_profits:
	print(i[0], "-->", i[1])
print('\n')
	
#Gets top stocks for bollinger 
sorted_b_profits = sorted(bProfits.items(), key=lambda x: x[1], reverse=True)
print("Best Stocks with Mean Reversion")
for i in sorted_b_profits:
	print(i[0], "-->", i[1])
print('\n')

#writes to JSON
saveResults(dictionary)


    

    




