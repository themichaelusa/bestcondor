import utils as ut
import pipeline as pl
import ironcondor as ic

def inputCondor():

	ticker = input("Please input a valid stock ticker. Example: GOOG, NVDA, NFLX ")
	print ("Please enter a valid Expiration Date. Example: 2017-3-17 ")

	year = input("Enter a Valid Year. Example: 2016 ")
	month = input("Enter a Valid Month. Example: 02 ")
	date = input("Enter a Valid Date. Example: 08 ")
	expDate = year + '-' + month + '-' + date

	return (str(ticker), str(expDate))

userInput = inputCondor()
opChain = pl.parseOptionsChain(userInput[0], userInput[1])
formattedOpChain = pl.formatOptionChain(opChain[0], opChain[1], opChain[2])

formattedCalls = ic.formatCalls(formattedOpChain[0])
formattedShortCalls = formattedCalls[0]
formattedLongCalls = formattedCalls[1]

formattedPuts = ic.formatPuts(formattedOpChain[1])
formattedShortPuts = formattedPuts[0]
formattedLongPuts = formattedPuts[1]
