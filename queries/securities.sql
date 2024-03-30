-- ***Securities Page***************************************************************************************************
-- *** Security Name Lookup *** -------------------------------------------------------------------------------------------
SELECT SecurityID
FROM Security
WHERE TICKER = { whatever Ticker is selected };

-- Test with Ticker = 'NASDAQ:AAPL'
SELECT SecurityID
FROM Security
WHERE TICKER = 'NASDAQ:AAPL';
-- Note: If we want to go extra, we might have to do error handling with this (i.e. throw an error for invalid ticker)
-- Also, the tickers in the DB include the exchange prepended. We can do some manipulations to separate
-- but I don't feel strongly about it. We can just ask the user to input the full ticker.

-- *** Security Name - Top of Page *** ---------------------------------------------------------------------------------
SELECT Name, Ticker
FROM Security
WHERE SecurityID = { whatever Security ID is selected };

-- Test with SecurityID = 1
SELECT Name, Ticker
FROM Security
WHERE SecurityID = 1;


-- *** Security Prices *** ---------------------------------------------------------------------------------------------
SELECT Date, Price
FROM SecurityPrice
WHERE SecurityID = { whatever Security ID is selected }
AND Date >= { whatever Start Date is selected, ensure date is in quotes }
AND Date <= { whatever End Date is selected ensure date is in quotes }
ORDER BY Date ASC;

-- Test with SecurityID = 1, Start Date = 2023-01-01, End Date = 2023-12-31
SELECT Date, Price
FROM SecurityPrice
WHERE SecurityID = 1
AND Date >= '2023-01-01'
AND Date <= '2023-12-31'
ORDER BY Date ASC;
-- Note: We may want to add validation to ensure that the start date and end date are reasonable
-- (i.e. end date is after start date, end date < today's date, start date > 2022-01-03, etc.)
-- I'm fine if we don't, but if there's an easy way to do it, we can add it.

-- *** Security Info *** -----------------------------------------------------------------------------------------------
WITH CurrencyLookup AS (
    SELECT *
    FROM Currency
)

SELECT Security.Name, Security.Type, Security.Ticker, Security.HQStreetAddress, Security.SharesOutstanding, Security.EPS, Security.Sectors, CurrencyLookup.CurrencyName
FROM Security
LEFT JOIN CurrencyLookup ON Security.CurrencyId = CurrencyLookup.CurrencyID
WHERE Security.SecurityID = { whatever Security ID is selected };


-- Test with SecurityID = 1
WITH CurrencyLookup AS (
    SELECT *
    FROM Currency
)

SELECT Security.Name, Security.Type, Security.Ticker, Security.HQStreetAddress, Security.SharesOutstanding, Security.EPS, Security.Sectors, CurrencyLookup.CurrencyName
FROM Security
LEFT JOIN CurrencyLookup ON Security.CurrencyId = CurrencyLookup.CurrencyID
WHERE Security.SecurityID = 1;

