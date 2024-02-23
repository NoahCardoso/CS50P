# STOCK TRACKER
### Video Demo:  <https://youtu.be/MlcDEk4hxSA>
### Description:
#### Overview
The project that I created is a stock manager tool (aka Stock Tracker). The program was made to be helpful in keeping track of your stock portfolio. What the program does is it allows you to see the current price of any stock (in the given list ) as well as buy, sell, or trade that stock. The program gives you a csv of the stocks, how much of that stock you own, its total value, and the price at the time you purchased that stock. You also have the option of entering a csv so you can edit a previous portfolio with the program and it will give the updated csv. To be clear this program does not buy stocks from the stock market or manage your actual money it is simply a fun way to keep track of the total value of all of the stocks that you currently own.

#### Challenges
Overall the process was very smooth except for getting the current stock prices. The only free url that I could find of which to get the current stock prices from had a limit of 25 requests per day. So I decided to add a `dict` of some stocks and their prices at the time. I have kept the function and it does work. In order to use it all you would have to do is replace all instances of `stock.price` with `stock.current_price`. Keep in mind that there is a 25-request limit per day so unless you have a url or way of getting current stock prices I wouldn't recommend using it.

#### Stock Class
The Stock class has 9 methods. Each stock object has two properties its name (Its four-digit NASDAQ symbol) and the amount of that stock you own. When you initialize a stock object it only requires a name as the default amount of a stock is zero. The most used method is the property price which returns the price of the stock.

#### Methods
`close(name, stocks)`
This method takes in the name of the csv file that you want to store your stock manager data on (The default name of the csv is `stock.csv`). stocks is a list of Stock objects that you have bought, sold or traded. Close uses a `DictWriter` to write the "name","price","quantity","total value" of each of the Stock objects to the csv however only if the total value of the stock is greater than zero.

`purchase(stock, n)`
This method takes in the current Stock object `stock` as well as `n` the amount of stock that the user wants to purchase. It calls the buy method from the Stock class which divides the money by the price of the stock and adds that number to the quantity of that stock.

`sell(stock, n)`
Similarly to purchase sell takes in the current Stock object `stock` and `n` the amount in USD that the user wants to sell. It calls the seller method from the Stock class which divides the money they entered by the price of that stock, subtracting the quantity of the stock by that difference.

`trade(stock, new_stock, n)`
It takes a stock object `stock` and the stock that you would like to obtain `new_stock` as well as `n` which is the amount in USD of stock that you want to trade for new_stock. It then sells n amount of stock and buys n amount of new_stock
