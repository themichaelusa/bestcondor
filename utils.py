import talib as tb
from talib import abstract
from talib.abstract import *

import numpy as np
import mibian as mb
import datetime as dt


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


def calculate_NATR(tb_input, timeperiod):

	natr = abstract.NATR
	return NATR(tb_input, timeperiod)


def get_greeks(stockPrice, strikePrices, interestRate, daysToExp, volNATR):

	callGreeks, putGreeks = [],[]

	for i in range(len(strikePrices)):

		strikePrice = strikePrices[i]
		opt = mb.BS([stockPrice, strikePrice, interestRate, daysToExp], volatility = volNATR)

		callGreeks.append((opt.callPrice, opt.callDelta, opt.callTheta))
		putGreeks.append((opt.putPrice, opt.putDelta, opt.putTheta))

	return (callGreeks, putGreeks)


def date_shift():

	currentDate = str(dt.date.today())
	dateOneYPrior = str(np.datetime64(currentDate) - np.timedelta64(365,'D'))

	curDY = str(currentDate[:4])
	curDM = str(currentDate[5:7])
	curDD = str(currentDate[8:10])

	priDY = str(dateOneYPrior[:4])
	priDM = str(dateOneYPrior[5:7])
	priDD = str(dateOneYPrior[8:10])

	return ((curDY, curDM, curDD, priDY, priDM, priDD))

	
def calculate_dateDistance(start_date, end_date):

	formatted_start = dt.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:10]))
	formatted_end = dt.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:10]))

	return np.busday_count(formatted_start,formatted_end)
	

def calculate_daysToExp(expy_date):	

	formatted_end = dt.date(int(expy_date[:4]), int(expy_date[5:7]), int(expy_date[8:10]))
	return np.busday_count(dt.date.today(), formatted_end, '1111111')







