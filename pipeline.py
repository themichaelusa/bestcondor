import json
import urllib
import mibian
import utils as ut
import pandas as pd
from distutils.util import strtobool

def pull_historical_data(ticker):

	# Date format: 'Year-Month-Date' --> '20170125'
	# Model URL = "http://real-chart.finance.yahoo.com/table.csv?s="+ ticker +"&d=2&e=01&f=2017&g=d&a=3&b=09&c=2012&ignore=.csv"

	dts = ut.date_shift() # url dates (start, end)
	urlTicker = "http://real-chart.finance.yahoo.com/table.csv?s=" + ticker
	urlDates =  '&d='+dts[2]+'&e='+dts[1]+'&f='+dts[0]+'&g=d&a='+dts[5]+'&b='+dts[4]+'&c='+dts[3]+'&ignore=.csv'
	url = urlTicker + urlDates
	dataframe = pd.read_csv(url)

	dataframe.rename(columns={'Adj Close':'AdjClose'}, inplace=True)
	dataframe['Datetime'] = pd.to_datetime(dataframe['Date'])
	dataframe = dataframe.set_index('Datetime')
	dataframe = dataframe.drop(['Date'], axis=1)
	dataframe = dataframe.drop(['Close'], axis=1)
	dataframe = dataframe.astype(float)
	dataframe = dataframe[['Open', 'AdjClose', 'High', 'Low', 'Volume']]

	nump_hist_data = dataframe.as_matrix(columns=None)

	talib_inputs = {
  	'open': nump_hist_data[0],
    'high': nump_hist_data[2],
    'low': nump_hist_data[3],
    'close': nump_hist_data[1],
    'volume': nump_hist_data[4]
	}

	return talib_inputs


def parseOptionsChain(ticker, expyDate):

	url = 'https://query2.finance.yahoo.com/v7/finance/options/' + ticker
	raw_data = urllib.urlopen(url).read()
	parsed_ticker_data = json.loads(raw_data)
	optionsJson = parsed_ticker_data['optionChain']['result'][0]
	optionsQuote = optionsJson['quote']

	strikes = optionsJson['strikes']
	strikesToInt = list(map(int, strikes))
	currentPrice = int(optionsQuote['regularMarketPrice'])
	truncatedStrikes = ut.truncate_strikes(strikesToInt, currentPrice)	

	historical_data = pull_historical_data(ticker)
	volatility = ut.calculate_NATR(historical_data, 14)
	daysToExp = ut.calculate_daysToExp(expyDate)
	interestRate = 0.98

	greeks = ut.get_greeks(currentPrice, truncatedStrikes, interestRate, daysToExp, volatility)  

	return (optionsJson, truncatedStrikes, greeks)
	

def formatOptionChain(optionsJson, truncatedStrikes):

	chainCalls = optionsJson['options'][0]['calls'] #append[i] to iterate through calls
	chainPuts = optionsJson['options'][0]['puts'] #append[i] to iterate through puts
	outputCalls, outputPuts = [],[]

	for i in range(len(chainCalls)):

		currentStrike = int(chainCalls[i]['strike'])

		if currentStrike in truncatedStrikes: 

			currentPrice = float(chainCalls[i]['lastPrice'])
			currentBid = float(chainCalls[i]['bid'])
			currentAsk = float(chainCalls[i]['ask'])
			currentIV = float(chainCalls[i]['impliedVolatility'])
			currentITM = str(bool(strtobool(str(chainCalls[i]['inTheMoney']))))

			if ((i == 0) or (i % 2 == 0)):
				floatStrike = float(currentStrike) + .5
				outputCalls.append((floatStrike, currentPrice, currentBid, currentAsk, currentIV, currentITM))

			elif ((i != 0) and (i % 2 != 0)): 
				outputCalls.append((currentStrike, currentPrice, currentBid, currentAsk, currentIV, currentITM))

	for i in range(len(chainPuts)):
		
		currentStrike = int(chainPuts[i]['strike'])

		if currentStrike in truncatedStrikes: 

			currentPrice = float(chainPuts[i]['lastPrice'])
			currentBid = float(chainPuts[i]['bid'])
			currentAsk = float(chainPuts[i]['ask'])
			currentIV = float(chainPuts[i]['impliedVolatility'])
			currentITM = str(bool(strtobool(str(chainPuts[i]['inTheMoney']))))

			if ((i == 0) or (i % 2 == 0)):
				outputPuts.append((currentStrike, currentPrice, currentBid, currentAsk, currentIV, currentITM))

			elif ((i != 0) and (i % 2 != 0)): 
				floatStrike = float(currentStrike) + .5
				outputPuts.append((floatStrike, currentPrice, currentBid, currentAsk, currentIV, currentITM))


	df_calls = pd.DataFrame.from_records(outputCalls, columns = ['Strike', 'Price', 'Bid', 'Ask', 'IV', 'ITM'])
	df_puts = pd.DataFrame.from_records(outputPuts, columns = ['Strike', 'Price', 'Bid', 'Ask', 'IV', 'ITM'])
	
	return (df_calls, df_puts)
