from yahoo_fin import stock_info as si
from datetime import datetime
import os
import argparse


os.system("")

class Style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'

class Stock():
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name
        self.quoteTable = si.get_quote_table(ticker)
    
    def current_price(self):
        quote_price = self.quoteTable.get('Quote Price')
        return str("{:.2f}".format(quote_price))

    def daily_change(self):
        quote_price = self.quoteTable.get('Quote Price')
        prev_close = self.quoteTable.get('Previous Close')
        daily_change = quote_price-prev_close
        daily_change_percent = (daily_change/prev_close)*100        
        
        # unicode up and down arrows for some prettier output!
        up_arrow_unicode = '\u2191'
        down_arrow_unicode = '\u2193'

        # if daily change is negative, return change in red text otherwise green
        if daily_change < 0:
            return str(Style.RED + down_arrow_unicode + " {:.2f}".format(daily_change) + " " + "({:.2f}%)".format(daily_change_percent) + Style.RESET)
        else:
            return str(Style.GREEN + up_arrow_unicode + " {:.2f}".format(daily_change) + " " + "({:.2f}%)".format(daily_change_percent) + Style.RESET)

    def __str__(self):
        ticker = self.ticker
        name = self.name
        price = self.current_price()
        change = self.daily_change()
        return f'{ticker:<10}{name:<40}{price:>10} {change:>20}'

def get_watchlist(watchlist_file):
    watchlist = []
    with open(watchlist_file, encoding='utf-8-sig') as f:
        for line in f:
            stock_info = line.split(',')
            try:
               stock = Stock(str.strip(stock_info[0]), str.strip(stock_info[1]))
            except IndexError:
                continue
            watchlist.append(stock)
    return watchlist

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('watchlist_file')
    args = parser.parse_args()
    watchlist_file = args.watchlist_file
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("TERMINAL_STOCK_QUOTE " + current_time + " watchlist: " + watchlist_file)
    for stock in get_watchlist(watchlist_file):
        print(stock)

if __name__ == '__main__':
    exit(main())
