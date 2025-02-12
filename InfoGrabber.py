import yfinance as yf
import pandas as pd
import time
import pprint
import requests
import ast
import ast
import requests
import tiktoken
enc = tiktoken.get_encoding("o200k_base")

FMP_apiKey = '7BTjYkVscGH0AdLI1KrxcRNqED9Q9ZwF'
def GetFinancialDataFMP(StockName, date, Type):
    with open('FinancialDataFMPFinancialsDatabase.txt', 'r') as f:
        FinancialDataFMPFinancialsDatabase = ast.literal_eval(f.read())
    if StockName + Type not in FinancialDataFMPFinancialsDatabase:
        Data = requests.get(f'https://financialmodelingprep.com/api/v3/{Type}/{StockName}?apikey={FMP_apiKey}').json()
        if Data != {'Error Message': 'Limit Reach . Please upgrade your plan or visit our documentation for more details at https://site.financialmodelingprep.com/'}:
            FinancialDataFMPFinancialsDatabase[StockName + Type] = Data
        with open('FinancialDataFMPFinancialsDatabase.txt', 'w') as f:
            pprint.pprint(FinancialDataFMPFinancialsDatabase, stream=f, width=200, indent=4)

    Document = FinancialDataFMPFinancialsDatabase[StockName + Type]

    closest_date = Document[-1]
    for x in reversed(range(len(Document))):
        if pd.to_datetime(Document[x]["date"]) <= pd.to_datetime(date):
            if pd.to_datetime(closest_date["date"]) < pd.to_datetime(Document[x]["date"]):
                closest_date = Document[x]
    for info in ["date", "symbol", "period", "reportedCurrency", "cik", "fillingDate", "acceptedDate", "calendarYear", "link", "finalLink"]:
        closest_date.pop(info)
    return closest_date

def GetStockInfo(stockName, date): 
    stockInformationDictionary = {}
    stock = yf.Ticker(stockName)
    currentPrice = stock.history(start=pd.to_datetime(date).tz_localize('America/New_York') - pd.DateOffset(days=5), end=date)
    stockInformationDictionary[0] = currentPrice['Close'].iloc[-1]
    
    stockHistory = stock.history(start=pd.to_datetime(date).tz_localize('America/New_York') - pd.DateOffset(years=2), end=pd.to_datetime(date).tz_localize('America/New_York'))  # PUT START AND END DATE INSTEAD NOWWW
    stockHistoryDictionary = {i+1: [row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Dividends'], row['Stock Splits']] for i, (index, row) in enumerate(stockHistory.iterrows())}
    for key in stockHistoryDictionary:
        for x in range(len(stockHistoryDictionary[key])):
            stockInformationDictionary[len(stockInformationDictionary)] = stockHistoryDictionary[key][x]  
    while len(stockInformationDictionary) != 3550:
        for x in range(len(stockHistoryDictionary[len(stockHistoryDictionary)])):
            stockInformationDictionary[len(stockInformationDictionary)] = stockHistoryDictionary[len(stockHistoryDictionary)][x]
            if len(stockInformationDictionary) == 3550:
                break

    """ GETTING YAHOO STOCK FINANCIALS
    # - balance sheet
    #pprint.pp(stock.balance_sheet)
    stock.balance_sheet
    stock.quarterly_balance_sheet
    # - cash flow statement
    stock.cashflow
    stock.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options
    quaterlyIncomeStatments = stock.quarterly_income_stmt.drop(stock.quarterly_income_stmt.columns[-1], axis=1)
    columns = quaterlyIncomeStatments.columns
    income_stmt_dict = {i+1: quaterlyIncomeStatments[col].tolist() for i, col in enumerate(columns)}
    for key in income_stmt_dict:
        for x in range(len(income_stmt_dict[key])):
            if math.isnan(income_stmt_dict[key][x]):
                stockInformationDictionary[len(stockInformationDictionary)] = 0.0
            else:
                stockInformationDictionary[len(stockInformationDictionary)] = float(income_stmt_dict[key][x])* 0.001"""
    
    #DONT ADD ABOVE
    IncomeStatement = GetFinancialDataFMP(stockName, date, "income-statement") #Instead of Document put the link to the data
    for key in IncomeStatement:
        stockInformationDictionary[len(stockInformationDictionary)] = IncomeStatement[key]
    BalanceSheet = GetFinancialDataFMP(stockName, date, "balance-sheet-statement") #Instead of Document put the link to the data
    for key in BalanceSheet:
        stockInformationDictionary[len(stockInformationDictionary)] = BalanceSheet[key]
    CashFlow = GetFinancialDataFMP(stockName, date, "cash-flow-statement") #Instead of Document put the link to the data
    for key in CashFlow:
        stockInformationDictionary[len(stockInformationDictionary)] = CashFlow[key]
    
    #24 2019-11-1 DATE WITH MOST
    # 4183
    CommoditiesStock = [
        yf.Ticker("CL=F"), yf.Ticker("KC=F"), yf.Ticker("NG=F"), yf.Ticker("GC=F"),  yf.Ticker("KE=F"), yf.Ticker("KE=F"), yf.Ticker("CT=F")
        ]
    for x in range(len(CommoditiesStock)):
        CommoStockHistory = CommoditiesStock[x].history(start= pd.to_datetime(date).tz_localize('America/New_York') - pd.DateOffset(months=1), end=pd.to_datetime(date).tz_localize('America/New_York')) # PUT START AND END DATE INSTEAD NOWWW
        CommoStockHistoryDictionary = {i+1: [row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Dividends'], row['Stock Splits']] for i, (index, row) in enumerate(CommoStockHistory.iterrows())}
        for key in CommoStockHistoryDictionary:
            for y in range(len(CommoStockHistoryDictionary[key])):
                stockInformationDictionary[len(stockInformationDictionary)] = CommoStockHistoryDictionary[key][y]

        while len(stockInformationDictionary) != 3664 + (161 * (x + 1)):
            for y in range(len(CommoStockHistoryDictionary[len(CommoStockHistoryDictionary)])):
                stockInformationDictionary[len(stockInformationDictionary)] = CommoStockHistoryDictionary[len(CommoStockHistoryDictionary)][y]
                if len(stockInformationDictionary) == 3664 + (161 * (x + 1)):
                    break  
    
    url = "https://data.alpaca.markets/v1beta1/news?end=" + str((pd.to_datetime(date) - pd.DateOffset(days=5)).strftime("%Y-%m-%d")) + "T00%3A00%3A00Z&sort=desc&symbols=" + stockName
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "PKMG98DX07QM5HFK0A2E",
        "APCA-API-SECRET-KEY": "EzCRW5QnqX1ZOMWNoYwNPOzL8gjmicQ0Ac4aVKKo"
    }

    response = requests.get(url, headers=headers)
    for x in range(3):
        for y in range(len(enc.encode(ast.literal_eval(response.text)['news'][x]['headline']))):
            stockInformationDictionary[len(stockInformationDictionary)] = enc.encode(ast.literal_eval(response.text)['news'][x]['headline'])[y]

        for y in range(len(enc.encode(ast.literal_eval(response.text)['news'][x]['summary'].replace('\r', '').replace('\n', '')))):
            stockInformationDictionary[len(stockInformationDictionary)] = enc.encode(ast.literal_eval(response.text)['news'][x]['summary'].replace('\r', '').replace('\n', ''))[y]

    while len(stockInformationDictionary) != 5010:
        stockInformationDictionary[len(stockInformationDictionary)] = 220

    return stockInformationDictionary

GetStockInfo("MSFT", "2023-01-08")

"""
#Go through dates to see if all dictionary size is the same
greatestNum = 5020
#greatestDate = []
for x in range(2019, 2025):
    if x == 2019:
        print(x)
        for y in range(10, 13):
            print(y)
            for z in range(1, 30, 5):
                stock = GetStockInfo("AAPL", str(x) + "-" + str(y) + "-" + str(z))
                if greatestNum != stock:
                    print("Error")
                    #greatestDate.append(str(x) + "-" + str(y) + "-" + str(z))
    elif x == 2024:
        print(x)
        for y in range(1, 6):
            print(y)
            for z in range(1, 30, 5):
                stock = GetStockInfo("AAPL", str(x) + "-" + str(y) + "-" + str(z))
                if greatestNum != stock:
                    print("Error")
                    #greatestDate.append(str(x) + "-" + str(y) + "-" + str(z))
    else:
        print(x)
        for y in range(1, 13):
            print(y)
            for z in range(1, 30, 5):
                stock = GetStockInfo("AAPL", str(x) + "-" + str(y) + "-" + str(z))
                if greatestNum != stock:
                    print("Error")
                    #greatestDate.append(str(x) + "-" + str(y) + "-" + str(z))

print(greatestNum)"""