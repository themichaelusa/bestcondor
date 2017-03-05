# Bestcondor

Simple Python 3.6 Script that automatically selects Short Iron Condors with optimal Risk/Reward Ratios and returns.
Useful tool in combination with Financial Time Series Analytics and ML to select spreads with high confidence.

## Installation And Usage

Download bestcondor.zip from repo page. Extract and cd into folder.
Type: ``` python3 condor.py ``` and enjoy!

## Documentation (for Modification)

### Basic Functions:

* `truncate_strikes(optionStrikes, stockPrice)`
* `get_strikes(tickerData)`
* `generateSpreads(OTMStrikes)`
* `generateIronCondor(spreads)`
* `outputCondors(ironCondors, ticker, expDate)`

## TODO

- [x] Truncate extraneous Call/Put Strikes
- [ ] PyPI support (pip install...)
- [ ] Functional Bear Call/Bull Put Spread Generation
- [ ] Functional Iron Condor Generation
- [ ] Output Optimal Short IC's
