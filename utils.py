import talib as tb
from talib import *
import numpy as np
import mibian as mb

def calculate_NATR(high, low, close, timeper):
	return tb.NATR(high, low, close, timeperiod = timeper)

def truncate_strikes(optionStrikes, stockPrice):

	osList = np.asarray(optionStrikes)
	idx = np.argmin(np.abs(osList - stockPrice))

	leftBound = osList[idx] - (osList[idx] * .05)
	rightBound = leftBound + (osList[idx] * .1)
	desiredIndices = []

	for i in range(len(optionStrikes)):
		if ((optionStrikes[i] <= rightBound) and (optionStrikes[i] >= leftBound)):
			desiredIndices.append(optionStrikes[i])
		else: continue

	return desiredIndices	

def get_greeks(stockPrice, strikePrices, interestRate, daysToExp, volNATR):

	callGreeks, putGreeks = [],[]

	for i in range(len(strikePrices)):

		strikePrice = strikePrices[i]
		opt = mb.BS([stockPrice, strikePrice, interestRate, daysToExp], volatility = volNATR)

		callGreeks.append((opt.callPrice, opt.callDelta, opt.callTheta))
		putGreeks.append((opt.putPrice, opt.putDelta, opt.putTheta))

	return (callGreeks, putGreeks)





