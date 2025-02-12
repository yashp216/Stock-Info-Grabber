import pprint
import requests
import ast
FMP_apiKey = '7BTjYkVscGH0AdLI1KrxcRNqED9Q9ZwF'

def GetFinancialDataFMP(StockName):
    #with open('FinancialDataFMPFinancialsDatabase.txt', 'r') as f:
    #    FinancialDataFMPFinancialsDatabase = ast.literal_eval(f.read())
    #if StockName + "income-statement" not in FinancialDataFMPFinancialsDatabase:
    FinancialDataFMPFinancialsDatabase = {}
    Data = [requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{StockName}?period=quarter?apikey={FMP_apiKey}').json(), requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{StockName}?apikey={FMP_apiKey}').json(), requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{StockName}?apikey={FMP_apiKey}').json()]
    for x in range(len(Data)):
        if Data[x] == {'Error Message': 'Limit Reach . Please upgrade your plan or visit our documentation for more details at https://site.financialmodelingprep.com/'}:
            print("LIMIT REACHED")
            return True
        FinancialDataFMPFinancialsDatabase[StockName + "income-statement"] = Data[0]
        FinancialDataFMPFinancialsDatabase[StockName + "balance-sheet-statement"] = Data[1]
        FinancialDataFMPFinancialsDatabase[StockName + "cash-flow-statement"] = Data[2]
        pprint.pp(FinancialDataFMPFinancialsDatabase)
        #with open('FinancialDataFMPFinancialsDatabase.txt', 'w') as f:
        #   pprint.pprint(FinancialDataFMPFinancialsDatabase, stream=f, width=200, indent=4)
        #return False

GetFinancialDataFMP("AAPL")

stockSymbolsDone = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "BRK.B", "V", "JNJ", "WMT", 
    "JPM", "NVDA", "UNH", "HD", "PG", "MA", "DIS", "PYPL", "VZ", "ADBE", 
    "NFLX", "KO", "PFE", "PEP", "MRK", "ABT", "T", "CMCSA", "INTC", "CSCO",
    "NKE", "XOM", "CRM", "WFC", "MCD", "ORCL", "ACN", "TMO", "QCOM", "COST",
    "DHR", "MDT", "LLY", "AVGO", "ABBV", "TXN", "HON", "PM", "BA", "UNP",
    "UPS", "BMY", "LIN", "IBM", "NEE", "AMAT", "SBUX", "MMM", "CAT", "LMT",
    "CVX", "GS", "DE", "BLK", "MS", "SYK", "AMGN", "ADP", "BKNG", "SPGI",
    "ISRG", "NOW", "ANTM", "LRCX", "MU", "GILD", "CI", "INTU"
]
stockSymbols = [
    "MDLZ", "GE",
    "CB", "SCHW", "CME", "FIS", "BDX", "AMT", "MMC", "EW", "APD", "PLD",
    "HUM", "NSC", "ADI", "CHTR", "EL", "SHW", "PNC", "CL", "ZTS", "MCO",
    "ICE", "D", "TGT", "TJX", "AON", "DG", "EXC", "MCK", "GM", "DUK",
    "SO", "PSA", "AEP", "WM", "ITW", "STZ", "ECL", "TRV", "AIG", "AZO",
    "VRTX", "FDX", "ALL", "ETN", "SRE", "ADSK", "CNC", "F", "GD", "A",
    "BSX", "AFL", "BIIB", "TFC", "BAX", "HSY", "SYY", "CARR", "EOG", "IDXX",
    "PRU", "KLAC", "HCA", "DD", "ILMN", "CDNS", "WELL", "RMD", "PH", "MTD",
    "KMB", "PAYX", "EBAY", "DOW", "YUM", "HIG", "DHI", "IQV", "OKE", "ROK",
    "TEL", "DTE", "PGR", "BXP", "SWK", "TT", "AEE", "BKR", "MSI", "NEM",
    "WST", "CPRT", "ANSS", "PPG", "CINF", "ROST", "NOC", "AVB", "RSG", "APTV",
    "AMP", "OTIS", "FTV", "CTAS", "LH", "FTNT", "CAG", "FRC", "TFX", "XYL",
    "PCAR", "IR", "CMS", "GWW", "ARE", "LEN", "KEYS", "NTRS", "FITB", "AWK",
    "WAB", "AES", "TYL", "BILL", "ESS", "ENPH", "VRSK", "CBRE", "MTB", "ZBRA",
    "MAS", "MKC", "SIVB", "HPE", "UAL", "CRL", "VMC", "SJM", "PEAK", "AKAM",
    "MKTX", "TFII", "RCL", "AVNT", "ULTA", "EXPE", "FMC", "TROW", "RE", "AJG",
    "COO", "HST", "FFIV", "LDOS", "ALGN", "TRMB", "CHD", "GRMN", "TTWO", "IP",
    "WEC", "AAP", "PFG", "BRO", "NRG", "UHS", "VRSN", "PPL", "WAT", "CAH",
    "VTR", "TSN", "IPG", "NI", "HOLX", "CTLT", "AOS", "WHR", "STE", "AVY",
    "RJF", "CMA", "FE", "FFIV", "IRM", "HII", "PKI", "LNT", "XRAY", "CBOE",
    "FDS", "CPT", "REG", "CF", "NVR", "OMC", "DOV", "XRAY", "ATO", "MKC",
    "LUMN", "JKHY", "STT", "HWM", "WRB", "VLO", "PKG", "LNC", "TRGP", "SLG"
]
Limit = False
for x in range(len(stockSymbols)):
    if Limit == True:
        break
    if x < 77:   
        print(stockSymbols[x])
        Limit = GetFinancialDataFMP(stockSymbols[x])
        if Limit == True:
            break