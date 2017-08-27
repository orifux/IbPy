import signal

from ib.opt import ibConnection, message
from ib.ext.Contract import Contract


def print_message_from_ib(msg):
    print(msg)
def price_handler(msg):
    if msg.field == 1:
        print("bid price = %s" % msg.price)
    elif msg.field == 2:
        print("ask price = %s" % msg.price)


def main():
    tws = ibConnection(port=7496,clientId=121)
    tws.registerAll(print_message_from_ib)
    tws.register(price_handler, message.closePrice)
    tws.connect()

    tick_id = 1
    c = Contract()
    c.m_symbol = 'AAPL'
    c.m_secType = 'STK'
    c.m_exchange = "SMART"
    c.m_currency = "USD"
    tws.reqMktData(tick_id, c, '', False)

    signal.pause()


if __name__ == '__main__':
    main()