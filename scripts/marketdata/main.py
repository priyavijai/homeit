import time
import argparse
from tickerinfo import TickerInfo

def process_tickers(tickers, filepath, append):
    '''Retrieves fundamental information from Finviz.com for each provided ticker and writes the data to the provided output file.'''
    f = open(filepath, "a" if append else "w")

    if not append:
        #        A      B           C    D       E        F    G      H        I        G          H          I     J         K    L            M        N     O       P        Q            R             S         T        U        V        W
        f.write("Ticker,Description,Link,Company,Industry,Type,Sector,Exchange,Category,Asset Type,Start Date,Trend,P/E Ratio,Beta,Dividend TTM,Dividend,Price,52W Low,52W High,Above Low By,Below High By,5Y Return,On 1000$,On 2000$,On 5000$,On 10000$\n")

    for ticker in tickers:
        ti = TickerInfo(ticker)

        if not ti.HasError:
            ti.print_file(f)

        time.sleep(0.1)

    f.close()

def load_tickers(filepath):
    '''Loads tickers from the provided input file. One ticker per line. Trailing and leading spaces are trimmed automatically.'''
    f = open(filepath, "r")
    tickers = []
    count = 0

    while True:
        line = f.readline()
        if not line:
            break
        count += 1
        ticker = line.strip()
        tickers.append(ticker)

    print(f"Loaded {count} tickers from file {filepath}")
    return tickers

def main():
    '''Loads tickers from the provided input file (one ticker per line) and outputs fundamental information about each ticker to the provided output file.'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--Append", action='store_true', help="Append output to existing file. Header line will be skipped.")
    parser.add_argument("-o", "--Output", action='store', required=True, help="File to write output to.")
    parser.add_argument("-i", "--Input", action='store', required=True, help="File to reach tickers from.")

    args = parser.parse_args()

    print(f"Append? {args.Append}")
    print(f"Input File: {args.Input}")
    print(f"Output File: {args.Output}")

    tickers = load_tickers(args.Input)
    process_tickers(tickers, args.Output, args.Append)

main()
