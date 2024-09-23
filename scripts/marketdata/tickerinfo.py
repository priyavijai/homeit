
import pandas as pd
import re
import time
import requests.exceptions
from finvizfinance.quote import finvizfinance

class TickerInfo:
    def extract_dividend(self, value):
        match = re.search("\((?P<divpercent>.*)%\)", value)
        if match is not None:
            divp = match.group("divpercent")
            try:
                v = float(divp)
                self.DividendPercentage = v
            except ValueError:
                self.DividendPercentage = 0
        else:
            self.DividendPercentage = 0
    def extract_type(self, value):
        if value is not None:
            if value.startswith("Closed-End Fund"):
                self.Type = "CEF"
            elif value.startswith("Exchange Traded Fund"):
                self.Type = "ETF"
            elif value.startswith("REIT"):
                self.Type = "REIT"
            else:
                self.Type = "Stock"
        else:
            self.Type = ""

    def extract_fundamental(self, key):
        if key in self._fundamentals:
            value = self._fundamentals[key]
            match key:
                case "Company":
                    self.Company = value
                case "Industry":
                    self.Industry = value
                    self.extract_type(value)
                case "Sector":
                    self.Sector = value
                case "Exchange":
                    self.Exchange = value
                case "Category":
                    self.Category = value
                case "Asset Type":
                    self.AssetType = value
                case "P/E":
                    self.PERatio = value
                case "Beta":
                    self.Beta = value
                case "Dividend TTM":
                    self.TTMDividend = value
                    self.extract_dividend(value)
                case "Price":
                    self.Price = value
                case "52W Range From":
                    self.Low52W = value
                case "52W Range To":
                    self.High52W = value
                case "52W Low":
                    self.Off52WLow = value
                case "52W High":
                    self.Off52WHigh = value
                case "Return% 5Y":
                    self.Return5Y = value

    def calculate_returns(self):
        self.Return1000 = self.DividendPercentage * 10
        self.Return2000 = self.DividendPercentage * 20
        self.Return5000 = self.DividendPercentage * 50
        self.Return10000 = self.DividendPercentage * 100

    def __init__(self, ticker):
        self.Ticker = ticker
        self.HasError = True
        self.Description = ""
        self.Link = "https://finviz.com/quote.ashx?t={ticker}&r=max&ty=l&ta=0&p=m".format(ticker=ticker)
        self.Company = ""
        self.Industry = ""
        self.Type = ""
        self.Sector = ""
        self.Exchange = ""
        self.Category = ""
        self.AssetType = ""
        self.PERatio = ""
        self.Beta = ""
        self.TTMDividend = ""
        self.Price = ""
        self.High52W = ""
        self.Low52W = ""
        self.Off52WHigh = ""
        self.Off52WLow = ""
        self.Return5Y = ""
        self.DividendPercentage = 0.0
        self.Return1000 = 0.0
        self.Return2000 = 0.0
        self.Return5000 = 0.0
        self.Return10000 = 0.0

        keys = ["Company", "Industry", "Sector", "Exchange", "Category", "Asset Type", "P/E", "Beta", "Dividend TTM",
                "Price", "52W Range From", "52W Range To", "52W Low", "52W High", "Return% 5Y"]

        try:
            stock = finvizfinance(ticker)
            self._fundamentals = stock.ticker_fundament()
            self.Description = stock.ticker_description()

            for key in keys:
                self.extract_fundamental(key)

            self.calculate_returns()
            self.HasError = False
            print(f"Finished fetching info for ticker {ticker}")
        except:
            print(f"Error fetching info for ticker {ticker}")

    def print_console(self):
        print(f"--------------------------------------------------------------------------------------------")
        print(f"Ticker: {self.Ticker}")
        print(f"Error: {self.HasError}")
        print(f"Description: {self.Description}")
        print(f"Link: {self.Link}")
        print(f"Company: {self.Company}")
        print(f"Industry: {self.Industry}")
        print(f"Sector: {self.Sector}")
        print(f"Exchange: {self.Exchange}")
        print(f"Category: {self.Category}")
        print(f"Asset Type: {self.AssetType}")
        print(f"P/E Ratio: {self.PERatio}")
        print(f"Beta: {self.Beta}")
        print(f"TTM Dividend: {self.TTMDividend}")
        print(f"DividendPercentage: {self.DividendPercentage}")
        print(f"Price: {self.Price}")
        print(f"52 Weeek High: {self.High52W}")
        print(f"52 Week Low: {self.Low52W}")
        print(f"Off 52W High: {self.Off52WHigh}")
        print(f"Off 52 Low: {self.Off52WLow}")
        print(f"5 Year Return: {self.Return5Y}")
        print(f"Return 1000$: {self.Return1000}")
        print(f"Return 2000$: {self.Return2000}")
        print(f"Return 5000$: {self.Return5000}")
        print(f"Return 10000$: {self.Return10000}")


    #    Ticker,Description,Link,Company,Industry,Type,Sector,Exchange,Category,Asset Type,
    #    Start Date,Trend,
    #    P/E Ratio,Beta,Dividend TTM,Dividend,Price,52W Low,52W High,Above Low By,Below High By, 5Y Return,
    #    DividendPercentage,On 1000$,,On 2000$,,On 5000$,On 10000$

    def print_file(self, file):
        file.write(f"{self.Ticker},\"{self.Description}\",{self.Link},{self.Company},{self.Industry},{self.Type},{self.Sector},{self.Exchange},{self.Category},{self.AssetType},")
        file.write(f"=TODAY()-5*365,fill trend formula,")
        file.write(f"{self.PERatio},{self.Beta},{self.TTMDividend},{self.DividendPercentage},{self.Price},{self.Low52W},{self.High52W},{self.Off52WLow},{self.Off52WHigh},{self.Return5Y},")
        file.write(f"{self.Return1000},{self.Return2000},{self.Return5000},{self.Return10000}")
        file.write(f"\n")
