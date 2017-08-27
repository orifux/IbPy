from ib.opt import Connection
from ib.ext.Contract import Contract
import time
import csv

Equity = Contract()
Equity.m_secType = 'Stk'
Equity.m_exchange = 'Smart'
Equity.m_currency = 'USD'

EquityList = ['XOM', 'JNJ', 'BRK B', 'JPM','GE','T','WFC','BAC','PG','CVX','VZ','PFE','MRK','HD','C','KO','DIS','V','UNH','PEP','PM','IBM','MO','SLB','ORCL','MMM','MDT','MA','WMT','MCD','ABBV','BMY','BA','HON','CVS','SPY']
PriceList = []
PriceData = csv.writer(open('/home/ori/price.csv','wb'))

def print_message_from_ib(msg):
    print(msg)
    

def savepx(msg):
    if msg.field == 4:
        PriceList.insert(msg.tickerId,msg.price)

def main():
    conn = Connection.create(port=7496,clientId=999)
    conn.registerAll(print_message_from_ib)
    conn.connect()
    count = 0
    for ticker in EquityList:
        Equity.m_symbol = ticker
        conn.register(savepx,'TickPrice')# move this out of loop, just do it once
        conn.reqMktData(count,Equity,225,True)#true snapshot
        #time.sleep(.15) #not needed unless over 50 messages per second
        #conn.cancelMktData(count) don't do this, use snapshot 
        #PriceList.insert(count,px) do in callback
        count = count + 1
        print count

    conn.disconnect()
    PriceData.writerow(EquityList)
    PriceData.writerow(PriceList)

main()