import math
import numpy as np
import datetime as dt

def truncateStrikes(optionStrikes, stockPrice):

	strikesToInt = list(map(float, optionStrikes))
	osList = np.asarray(strikesToInt)
	idx = np.argmin(np.abs(osList - stockPrice))

	leftBound = osList[idx] - (osList[idx] * .05)
	rightBound = leftBound + (osList[idx] * .1)
	desiredIndices = []

	for i in range(len(strikesToInt)):
		if ((strikesToInt[i] <= rightBound) and (strikesToInt[i] >= leftBound)):
			desiredIndices.append(strikesToInt[i])
		else: continue

	return desiredIndices


def calculateDelta(optionPrice, stockPrice):

	stockPriceDiff = stockPrice *.1
	return ((optionPrice * (stockPrice + stockPriceDiff)) - (optionPrice * stockPrice))/stockPriceDiff


def formatExpiryURL(expDate):

	formattedStart = dt.date(1970, 01, 01)
	formattedEnd = dt.date(int(expDate[:4]), int(expDate[5:7]), int(expDate[8:10]))
	return 86400 * (np.busday_count(formattedStart, formattedEnd, '1111111'))
