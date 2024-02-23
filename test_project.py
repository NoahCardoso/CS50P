from project import seller, purchase, trade, Stock
DATA={"AMZN": "149.20", "AAPL": "184.25", "MSFT": "370.60", "GOOG": "138.92", "TSLA": "241.08", "IBM": "161.52", "XRX": "16.48", "TXN": "164.60" }
def test_purchase():
    stock=Stock("AMZN")
    purchase(stock, 10*149.2)
    assert stock.total_value == 1492
def test_seller():
    stock=Stock("AMZN", 10)
    seller(stock, 10*149.2)
    assert stock.total_value == 0
def test_trade():
    stock=Stock("AMZN", 10)
    new_stock=Stock("AAPL", 2)
    trade(stock,new_stock,5*149.2)
    assert new_stock.total_value==2*184.25+5*149.2
