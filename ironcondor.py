import wallstreet
import numpy as np
import utils as ut
import pipeline as pl
from wallstreet import Stock, Call, Put

def input_condor():

	ticker = input("Please input a valid stock ticker. Example: GOOG, NVDA, NFLX ")
	print ("Please enter a valid Expiration Date. Example: 2017-3-17 ")

	year = input("Enter a Valid Year. Example: 2016 ")
	month = input("Enter a Valid Month. Example: 12 ")
	date = input("Enter a Valid Date. Example: 2 ")
	
	return (str(ticker), int(date), int(month), int(year))


def get_strikes(tData, isIndex):

	stock, expD, expM, expY = tData[0], tData[1], tData[2], tData[3]
	stockPrice = Stock(tData[0]).price	
	sCall, lCall, sPut, lPut = [],[],[],[]

	desiredStrikes = pl.pullOptionsChain(stock, True)

	for i in range(len(desiredStrikes)):

		strikePos = desiredStrikes[i]

		currentCall = Call(stock, d = expD, m = expM, y = expY, strike = strikePos)
		currentCallDelta = (1 - currentCall.delta())
		sCallDeltaValid = currentCallDelta >= 76.000 and currentCallDelta <= 80.000
		lCallDeltaValid = currentCallDelta > 80.000 and currentCallDelta <= 84.000

		currentPut = Put(stock, d = expD, m = expM, y = expY, strike = strikePos)
		currentPutDelta = (currentPut.delta() - 1)
		sPutDeltaValid = currentPutDelta <= -76.000 and currentPutDelta >= -80.000
		lPutDeltaValid = currentPutDelta < -80.000 and currentPutDelta >= -84.000

		validDeltas = (sCallDeltasValid and lCallDeltaValid and sPutDeltaValid and lPutDeltaValid)

		if not validDeltas: continue

		else:
			if (sCallDeltasValid):
				sCall.append(strikePos)
			elif (lCallDeltaValid):
				lCall.append(strikePos)

			if (sPutDeltaValid):
				sPut.append(strikePos)
			elif (lPutDeltaValid):
				lPut.append(strikePos)

	return (sCall, lCall, sPut, lPut)


def generate_spreads(OTM_Strikes):

	bearCallSpreads, bullPutSpreads = [],[]

	# generates all valid Bear Call Spreads
	for i in range(len(OTM_Strikes[0])):
		for j in range(len(OTM_Strikes[1])):
			if (OTM_Strikes[1][j].strikes > OTM_Strikes[0][i].strikes):
				bearCallSpreads.append((OTM_Strikes[0][i],OTM_Strikes[1][j]))
			else: continue

	# generates all valid Bull Put Spreads
	for i in range(len(OTM_Strikes[2])):
		for j in range(len(OTM_Strikes[3])):
			if (OTM_Strikes[3][j].strikes > OTM_Strikes[2][i].strikes):
				bullPutSpreads.append((OTM_Strikes[2][i],OTM_Strikes[3][j]))
			else: continue

	return (bearCallSpreads, bullPutSpreads)


def generate_ironcondor(spreads):

	ic_list = []

	for i in range(len(spreads[0])):
		for j in range(len(spreads[1])):
			upperBound = spreads[0][i]
			lowerBound = spreads[1][j]
			if ((upperBound[0] > lowerBound[0]) and (upperBound[1] > lowerBound[1])):
				ic_list.append((lowerBound[1], lowerBound[0], upperBound[1], upperBound[0]))
			else: continue

	return ic_list	


def output_condors(iron_condors, ticker, exp_date):

	print('Top Iron Condors for ' + ticker + ' at: ' + exp_date)
	for i in range(len(iron_condors)):
		print('temp')

	return 'temp'
