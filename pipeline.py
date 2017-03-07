import json
import urllib
import mibian
import utils as ut

def pullOptionsChain(ticker, pullStrikes):

	url = 'https://query2.finance.yahoo.com/v7/finance/options/' + ticker
	raw_data = urllib.urlopen(url).read()
	parsed_ticker_data = json.loads(raw_data)
	optionsJson = parsed_ticker_data['optionChain']['result'][0]
	optionsQuote = optionsJson['quote']

	currentPrice = int(optionsQuote['regularMarketPrice'])
	currentHigh = int(optionsQuote['regularMarketHigh'])
	currentLow = int(optionsQuote['regularMarketLow'])
	volatility = ut.calculate_NATR(currentHigh, currentLow, currentPrice, 14)
	interestRate = 0.98

	strikes = optionsJson['strikes']
	strikesToInt = list(map(int, strikes))
	truncatedStrikes = ut.truncate_strikes(strikesToInt, currentPrice)
	if(pullStrikes == True): return truncatedStrikes

	chainCalls = optionsJson['options'][0]['calls'] #append[i] to iterate through calls
	chainPuts = optionsJson['options'][0]['puts'] #append[i] to iterate through puts
	outputCalls, outputPuts = [],[]

	for i in range(len(chainCalls)):
		currentStrike = chainCalls[i]['strike']
		if ccurrentStrike in truncatedStrikes: 
			outputCalls.append((currentPrice, currentStrike,))
		elif currentStrike not in truncatedStrikes: continue 

	for i in range(len(chainPuts)):
		currentStrike = chainPuts[i]['strike']
		if currentStrike in truncatedStrikes: 
			outputPuts.append((currentPrice,currentStrike,))
		elif currentStrike not in truncatedStrikes: continue 

	return (chainCalls, chainPuts)


def formatOptionChain():
	return 'temp'



# d1 = numerd1 / (sigma * scipy.sqrt(T - time)[:, scipy.newaxis])
# from scipy.stats import norm
# Delta = norm.cdf(d1)