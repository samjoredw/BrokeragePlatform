-- ***Trade Page***************************************************************************************************
-- *** Check Current Security Price ***
-- Because this uses CURRENT_DATE you'll need to append the new prices for this to work, but you can test it using an old date.
-- Note some weekend dates or holiday dates may not work as prices are not present for those days.
-- Also, you'll need to add the transaction to the Transaction and Holding tables and update the cash balance in the account.
-- We'll need to multiply the current price by number of shares input by user to get the total value.

-- Get temporary table of security prices for today and check against ticker input by user.
WITH TodayPrices AS (
    SELECT SecurityID, Price
    FROM SecurityPrice
    WHERE Date = CURRENT_DATE
), SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
)
SELECT SecurityInfo.SecurityID, SecurityInfo.Ticker, SecurityInfo.Name, TodayPrices.Price
FROM SecurityInfo
LEFT JOIN TodayPrices ON SecurityInfo.SecurityID = TodayPrices.SecurityID
WHERE SecurityInfo.Ticker = { whatever Security ticker is input by user };



-- Test with AAPL and a date where the price is present (2023-01-03)
WITH TodayPrices AS (
    SELECT SecurityID, Price, Date
    FROM SecurityPrice
    WHERE Date = '2023-01-03'
), SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
)
SELECT SecurityInfo.SecurityID, SecurityInfo.Ticker, SecurityInfo.Name, TodayPrices.Price, TodayPrices.Date
FROM SecurityInfo
LEFT JOIN TodayPrices ON SecurityInfo.SecurityID = TodayPrices.SecurityID
WHERE SecurityInfo.Ticker = 'NASDAQ:AAPL';

-- ***Check Account Cash Balance***************************************************************************************************
-- Note: I don't know how exactly you're implementing the front end, so there may be a separate query necessary to lookup the account ID.
-- This should be straightforward to implement though.
SELECT AccountID, AccountType, CashBalance
FROM Account
WHERE AccountID = { whatever Account ID is selected };

-- Test with AccountID = 1
SELECT AccountID, AccountType, CashBalance
FROM Account
WHERE AccountID = 1;






-- ***Check Account Holdings Security Balance***************************************************************************************************
-- Note: I don't know how exactly you're implementing the front end, so there may be a separate query necessary to lookup the account ID.
-- This should be straightforward to implement though.
WITH AccountHoldings AS (
    SELECT AccountID, SecurityID, ShareCount
    FROM Holding
    WHERE AccountID = { whatever Account ID is selected }
), SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
    WHERE Ticker = { whatever Security ticker is input by user }
), SummedHoldings AS (
    SELECT AccountID, SUM(ShareCount) AS TotalShareCount
    FROM AccountHoldings
    GROUP BY AccountID
)
SELECT SummedHoldings.AccountID, SecurityInfo.Ticker, SecurityInfo.Name, SummedHoldings.TotalShareCount
FROM SummedHoldings
LEFT JOIN SecurityInfo ON SummedHoldings.AccountID = SecurityInfo.SecurityID;


-- Test with AccountID = 1 and ticker = 'SPY'
WITH AccountHoldings AS (
    SELECT AccountID, SecurityID, ShareCount
    FROM Holding
    WHERE AccountID = 1
), SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
    WHERE Ticker = 'SPY'
), SummedHoldings AS (
    SELECT AccountHoldings.AccountID, AccountHoldings.SecurityID, SUM(ShareCount) AS TotalShareCount
    FROM AccountHoldings
    GROUP BY AccountHoldings.AccountID, AccountHoldings.SecurityID
)
SELECT SummedHoldings.AccountID, SecurityInfo.Ticker, SecurityInfo.Name, SummedHoldings.TotalShareCount
FROM SummedHoldings
LEFT JOIN SecurityInfo ON SummedHoldings.SecurityID = SecurityInfo.SecurityID;
