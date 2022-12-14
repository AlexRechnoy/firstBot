from bs4 import BeautifulSoup
import requests

def getAllCurrencies():
    ##########
    def getBankData(bankSection):
        def getExchangeRate(bankSection,currencyCode : str):
            cashSections = bankSection.findAll('div', {'data-currencies-code': currencyCode})
            for tekSection in cashSections:
                if 'data-currencies-rate-buy' in tekSection.attrs:
                    buy=float(tekSection.attrs['data-currencies-rate-buy'])
                if 'data-currencies-rate-sell' in tekSection.attrs:
                    sell= float(tekSection.attrs['data-currencies-rate-sell']) # такого вида "data-currencies-rate-sell="71.49""
            return buy,sell
        bankName = (bankSection.find('a').contents[0])  # название банка такого вида : data-currencies-bank-name>Камкомбанк</a>
        timeSection=bankSection.find('div',class_='trades-table__refresh-time')
        exchangeTime=timeSection.find('span',{'class': 'text-nowrap'}).contents[0]
        buyE, sellE = getExchangeRate(bankSection,'EUR')
        buyU, sellU = getExchangeRate(bankSection,'USD')
        return buyE, sellE, buyU, sellU, bankName, exchangeTime
    ##########
    h = {'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 107.0.0.0 Safari / 537.36'}
    url = 'https://www.banki.ru/products/currency/cash/moskva/#bank-rates'
    r = requests.get(url, headers=h)
    soup = BeautifulSoup(r.content, 'html.parser')
    cash_table_section = soup.findAll('div', {'data-test': 'exchange-row'})
    banksData=[]
    for bankSection in cash_table_section:
        buyE, sellE, buyU, sellU, bankName, exchangeTime=getBankData(bankSection)
        if (buyE<10) or (sellE<10) or (buyU<10) or (sellU<10):
            continue
        bankData={'name': bankName,'eur''sale':sellE,'eur''buy' : buyE,'usd''sale':sellU,'usd''buy':buyU,'time':exchangeTime}
        banksData.append(bankData)
    return banksData