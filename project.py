#Stock manager
#By Noah Cardoso


import sys
import csv
import requests

#consts
API_KEY = ""
DATA={"AMZN": "149.20", "AAPL": "184.25", "MSFT": "370.60", "GOOG": "138.92", "TSLA": "241.08", "IBM": "161.52", "XRX": "16.48", "TXN": "164.60" } #for testing

class Stock:

    def __init__(self, name, quantity=0):
        #self.name
        #self.quantity
        self._name=name
        self._quantity=float(f"{(quantity):.4f}")

    def buy(self, n): #n represents amount in USD
        amount=n/self.price
        if amount<=0:
            raise ValueError("Insufficient Funds")
        self.add(amount)

    def add(self, n):
        if n<=0:
            raise ValueError("Insufficient Funds")
        self._quantity+=n

    def sell(self, n):
        if n<=0:
            raise ValueError("Insufficient Funds")
        if self.total_value-n>=0:
            x=n/self.price
            self._quantity-=x
        else:
            raise ValueError("")

    #25 request limit per day. Only use if have vaild URL
    @property
    def current_price(self):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.name}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if "Global Quote" in data:
            current_cost = data["Global Quote"]
            if "05. price" in current_cost:
                return float(current_cost["05. price"])
            else:
                print("Price not available")
                raise ValueError
        else:
            print("Data not available")
            raise ValueError

    @property
    def price(self):
        if self.name in DATA:
            cost=float(DATA[self.name])
        else:
            raise ValueError("Data not available")
        return cost
    @property
    def name(self):
        return self._name
    @property
    def quantity(self):
        return float(f"{(self._quantity):.4f}")
    @property
    def total_value(self):
        n=self.price
        n=n*self._quantity
        return float(f"{n:.4f}")

def main():
    #list of users stock objects
    stocks=[]

    #adds any stocks to list of stocks if given csv file
    if len(sys.argv)!=1 and len(sys.argv)!=2:
        sys.exit("Invaild command line arguments")
    if len(sys.argv)==2:
        try:
            file=open(sys.argv[1])
            reader=csv.DictReader(file)
            for row in reader:
                stocks.append(Stock(row["name"],float(row["quantity"])))
        except FileNotFoundError:
            sys.exit("Cannot open file")

    #tells user how to exit loop
    print("")
    print("Enter ctr+d when finished to see csv of all of the stock you own")
    print("")

    #main gameplay loop
    while True:
        try:
            print("")
            #checks if stock is allready in list of stocks
            tag=input("Enter NASDAQ ticker symbol (name) of a stock : ").upper()
            tags=[]
            for s in stocks:
                if s.name not in tags:
                    tags.append(s.name)

            #if it list of stocks set the current stock object to that stock
            if tag in tags:
                stock=stocks[tags.index(tag)]

            #otherwise add it to the list
            else:
                stock=Stock(tag)
                stocks.append(stock)


            print(f"The current price of {stock.name} is: {stock.price} USD")

            #prompts user
            print("1. Buy || 2. Sell || 3. Trade")
            text=input("(1,2,3): ")

            #buying
            if text=="1" or text.lower()=="buy":
                while True:
                    purchase(stock, input(f"how much of {stock.name} would you like to buy (USD): $"))
                    print(f"You have bought {stock.quantity} stock(s) of {stock.name}")
                    ans=input("Would you like to buy more? (y/n): ")
                    if ans.lower()!="y":
                        break

            #selling
            elif text=="2" or text.lower()=="sell":
                if stock.total_value>0:
                    while True:
                        seller(stock,input(f"how much of {stock.name} would you like to sell (USD): $").upper())
                        print(f"You now have {stock.quantity} stock(s) of {stock.name}")
                        ans=input("Would you like to sell more? (y/n): ")
                        if ans.lower()!="y":
                            break
                else:
                    print(f"You do not own any {stock.name} stock")

            #tradeing
            elif text=="3" or text.lower()=="trade":
                if stock.total_value>0:
                    while True:
                        try:
                            new_stock=input(f"Enter NASDAQ of stock you would like to trade for your {stock.name} stock: ").upper()
                            if new_stock == stock.name:
                                print("Must Trade for diffrent stock")
                                raise ValueError
                            if new_stock in tags:
                                new_stock=stocks[tags.index(new_stock)]
                            else:
                                new_stock = Stock(new_stock)
                                stocks.append(new_stock)
                            print(f"|SELLING| The current price of {stock.name} is {stock.price} USD.   You have {stock.total_value}")
                            print(f"|BUYING| The current price of {new_stock.name} is {new_stock.price} USD.    You have {new_stock.total_value}")
                            print("")
                            n=input(f"how much of {stock.name} would you like to sell (USD): $")
                            trade(stock,new_stock,n)
                            print(f"You now have {stock.quantity} stock(s) of {stock.name}")
                            print(f"You now have {new_stock.quantity} stock(s) of {new_stock.name}")
                            ans=input("Would you like to trade more? (y/n): ")
                            if ans.lower()!="y":
                                break
                        except ValueError:
                            print("ERROR please try again")
                else:
                    print(f"You do not own any {stock.name} stock")

        except ValueError:
            print("ERROR data not avalible")
            print("Try again")
        except EOFError:
                if len(sys.argv)==2:
                    close(sys.argv[1],stocks)
                else:
                    close("stock.csv",stocks)
                break


#returns csv of all stocks
def close(name,stocks):
    with open(name, "w") as file:
        writer=csv.DictWriter(file, fieldnames=["name","price","quantity","total value"])
        writer.writerow({"name": "name", "price": "price", "quantity": "quantity", "total value": "total value"})
        for s in stocks:
            #only write to csv if you still own any of the stock
            if s.total_value!=0:
                writer.writerow({"name": s.name, "price": s.price, "quantity": s.quantity, "total value": s.total_value})

#buys more of a stock
def purchase(stock, n):
        try:
            stock.buy(float(n))
        except ValueError:
            print("Insufficient Funds")

#sells n number of stock where n is money in USD
def seller(stock,n):
        try:
            stock.sell(float(n))
        except ValueError:
            print("Insufficient Funds")

#sells one stock for a new_stock
def trade(stock, new_stock, n):
        try:
            n=float(n)
            stock.sell(n)
            new_stock.buy(n)
        except TypeError:
            print("Invalid number")



if __name__ == "__main__":
    main()
