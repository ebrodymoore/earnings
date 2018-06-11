import pandas as pd
import numpy as np
import requests
import sys
from twilio.rest import Client
import datetime

#input for stock symbols
todayStocks = []
response = 'placeholder'
while response != 'done':
	response = raw_input("Enter symbol (lowercase acceptable) or 'done': ")
	if response != 'done':
		todayStocks.append(response)

#function to retrieve stock symbols from alphavantage
def APIpull (stockSymbol):
	
	#put together URL
	alphavantage_apikey = ''
	function = 'TIME_SERIES_DAILY'
	outputsize = 'compact'
	symbol = stockSymbol
	datatype = 'csv'
	URL = "https://www.alphavantage.co/query?function=" + function + "&symbol=" + symbol + "&outputsize=" + outputsize + "&apikey=" + alphavantage_apikey + "&datatype=" + datatype
	
	#call API and put into df
	df = pd.read_csv(URL)

	#calculating day over day return for each symbol
	df = df.reindex(index=df.index[::-1])
	df[stockSymbol] = df.close.pct_change()
	df = df.reindex(index=df.index[::-1])

	return df

#list market indicators to use (requires 2)
marketSymbols = ['VFINX', 'QQQ']

#pass market indicators through function; save to marketData
marketData = pd.DataFrame()
for i in marketSymbols:
	i = APIpull(i)
	marketData = pd.concat([marketData, i[:20]], axis=1)

#calculate market return and store in marketReturn
marketData = marketData[marketSymbols]
marketData['marketReturn'] = marketData.mean(axis=1)

#create market return stats
avgMarketReturn = marketData['marketReturn'].mean()
stdMarketReturn = marketData['marketReturn'].std()

#retrieve earnings stocks and save as df
earningsSymbols = todayStocks

#pass stock symbols with earnings call today through function
stockData = pd.DataFrame()
for i in earningsSymbols:
	i = APIpull(i)
	stockData = pd.concat([stockData, i[:20]], axis=1)
stockData = stockData[earningsSymbols]

#find correlations between market returns and each stock
correlations = pd.DataFrame()

for column in stockData:
	correlation = marketData['marketReturn'].corr(stockData[column])
	correlations = correlations.append({column: correlation}, ignore_index=True) 

#figure out which stocks are worthy
final = []

for column in stockData:
	if stockData[column].mean() > avgMarketReturn:
		if correlations[column].sum() < .5:
			final.append(column)
	else:
		#final.append('none')
		continue

#setup text message
today = datetime.datetime.today().strftime('%b %d')
text = ', '.join(final)
text = text.upper()
text = "Stocks with expected positive earnings announcements for "+today+' are: '+text

#confirm to send text
confirmation = ''

while response != 'GO':
	response = raw_input("You're about to send the text. Enter 'GO' to proceed: ")
	if response != 'GO':
		sys.exit()
	else:
		print('The text is on its way')
		continue

# Your Account SID from twilio.com/console
account_sid = ""
# Your Auth Token from twilio.com/console
auth_token  = ''

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+", 
    from_="+",
    body=text)