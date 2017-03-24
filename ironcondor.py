import utils as ut
import pipeline as pl

def formatCalls(inputCalls):

	sCall, lCall = [],[]

	for i in range(len(inputCalls)):

		currentCallProbOTM = inputCalls[i].currentProbOTM
		sCallDeltaValid = currentCallProbOTM >= .55 and currentCallProbOTM <= .80
		lCallDeltaValid = currentCallProbOTM > .80 and currentCallProbOTM <= .99

		validDeltas = (sCallDeltaValid or lCallDeltaValid)

		if not validDeltas: continue

		else:
			if (sCallDeltaValid):
				sCall.append(inputCalls[i])
			elif (lCallDeltaValid):
				lCall.append(inputCalls[i])

	return (sCall, lCall)


def formatPuts(inputPuts):

	sPut, lPut = [],[]

	for i in range(len(inputPuts)):

		currentPutProbOTM = inputPuts[i].currentProbOTM
		sPutDeltaValid = currentPutProbOTM >= .55 and currentPutProbOTM <= .80
		lPutDeltaValid = currentPutProbOTM > .80 and currentPutProbOTM <= .99

		validDeltas = (sPutDeltaValid or lPutDeltaValid)

		if not validDeltas: continue

		else:
			if (sPutDeltaValid):
				sPut.append(inputPuts[i])
			if (lPutDeltaValid):
				lPut.append(inputPuts[i])	

	sPut.reverse()
	lPut.reverse()

	return (sPut, lPut)


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
