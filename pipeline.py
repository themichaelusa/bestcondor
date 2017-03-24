import json
import urllib
import utils as ut
from distutils.util import strtobool


class Call(object):
	"""docstring for Call"""
	def __init__(self, currentStrike, currentPrice, currentProbOTM, currentIV, currentITM):

		self.currentStrike = currentStrike
		self.currentPrice = currentPrice
		self.currentProbOTM = currentProbOTM
		self.currentIV = currentIV
		self.currentITM = currentITM


class Put(object):
	"""docstring for Put"""
	def __init__(self, currentStrike, currentPrice, currentProbOTM, currentIV, currentITM):
		
		self.currentStrike = currentStrike
		self.currentPrice = currentPrice
		self.currentProbOTM = currentProbOTM
		self.currentIV = currentIV
		self.currentITM = currentITM


def parseOptionsChain(ticker, expDate):

	urlTicker = 'https://query2.finance.yahoo.com/v7/finance/options/' + ticker
	urlDate = '?date=' + str(ut.formatExpiryURL(expDate))
	url = urlTicker + urlDate

	rawData = urllib.urlopen(url).read()
	parsedTickerData = json.loads(rawData)
	optionsJson = parsedTickerData['optionChain']['result'][0]
	optionsQuote = optionsJson['quote']

	strikes = optionsJson['strikes']
	currentStockPrice = float(optionsQuote['regularMarketPrice'])
	truncatedStrikes = ut.truncateStrikes(strikes, currentStockPrice)	

	return (optionsJson, truncatedStrikes, currentStockPrice)
	

def formatOptionChain(optionsJson, truncatedStrikes, currentStockPrice):

	chainCalls = optionsJson['options'][0]['calls'] #append[i] to iterate through calls
	chainPuts = optionsJson['options'][0]['puts'] #append[i] to iterate through puts
	outputCalls, outputPuts = [],[]

	for i in range(len(chainCalls)):

		currentStrike = (chainCalls[i]['strike'])

		if currentStrike in truncatedStrikes: 

			currentPrice = float(chainCalls[i]['lastPrice'])
			currentIV = float(chainCalls[i]['impliedVolatility'])
			currentITM = str(bool(strtobool(str(chainCalls[i]['inTheMoney']))))
			currentProbOTM = (1 - ut.calculateDelta(currentPrice, currentStockPrice))

			outputCalls.append(Call(currentStrike, currentPrice, currentProbOTM, currentIV, currentITM))

	for i in range(len(chainPuts)):
		
		currentStrike = (chainPuts[i]['strike'])

		if currentStrike in truncatedStrikes: 

			currentPrice = float(chainPuts[i]['lastPrice'])
			currentIV = float(chainPuts[i]['impliedVolatility'])
			currentITM = str(bool(strtobool(str(chainPuts[i]['inTheMoney']))))
			currentProbOTM = (1 - ut.calculateDelta(currentPrice, currentStockPrice))

			outputPuts.append(Put(currentStrike, currentPrice, currentProbOTM, currentIV, currentITM))
	
	return (outputCalls, outputPuts)
