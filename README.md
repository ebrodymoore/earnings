# earnings
Text recommendations for executing post-earnings announcement drift investment strategy

Steps:
1. Enter into terminal the stock symbols for earnings announcements (same day ideally)
2. Ingests historical stock data from Alphavantage API, along with market-wide data
3. Puts stock symbols through parameters relating to the market
4. Text messages the buy recommendations (those that are expected to have a positive earnings announcement) through Twilio API
