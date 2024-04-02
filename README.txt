BROKERAGE PLATFORM WEB APPLICATION README FILE
================================================================================================================================================

Database Name: proj1part2
PostgreSQL Account: se2584:se2584
URL of Web Application: https://brokerage-platform-2aa42e36053e.herokuapp.com/

Please note that this applications origin and its database are stored on a VM but it is being hosted on heroku. (Given permission by TA)

**************************************************************************************************************************************************
Implementation vs. Proposal:
We included all of the entities from the proposal, and added an additional table "currencyrate" to store a time series of currency prices.

The app allows a user to select from various accounts, view holdings, view past transactions, view past transfers, view past transactions, view a personal profile, and view security profiles including historical prices.

While we did not implement a sophisticated authorization mechanism, the initial screen has a simple "login" screen.

All of the data is internally consistent. For example, past transactions use historically accurate security and currency prices. Additionally, each account needed to have enough securities and cash to complete the historical transactions.

For example, for transaction ID 3 which was executed by accountID 6, the per share price of the security was 98.19 and the share count was 10. The account needed to have at least $981.90 in the account at transaction time.

Because of time constraints and certain technical issues, we did not integrate functions to execute transactions, execute transfers, and edit the profile into the front end. However, the associated SQL queries to do so would be the following:

-- ***Update User Profile*******************************************
-- Generic query
UPDATE "user"
SET FirstName = {FirstName input by user}, LastName = {LastName input by user}, DateOfBirth = {DOB input by user},
StreetAddress = {StreetAddress input by user}, City = {City input by user}, Zip = {Zip input by user}, Country = {Country input by user},
PhoneNumber = {PhoneNumber input by user}, BankAccountRouting = {BankAccountNumber input by user}, BankAccountNumber = {BankAccountNumber input by user}
WHERE UserID = {UserID applicable};

-- Query using sample values
UPDATE "user"
SET FirstName = 'Tom', LastName = 'Riddle', DateOfBirth = '1985-01-01', StreetAddress = '24 Columbia Drive', City = 'New York', Zip = 10005, Country = 'USA', PhoneNumber = '917-999-1234', BankAccountRouting = 123456789, BankAccountNumber = 987654321
WHERE UserID = 1;

-- ***Execute Transfer*******************************************
-- Generic query
BEGIN TRANSACTION;

-- Only check balance if the transfer is negative
IF {the amount to transfer} < 0 AND (SELECT CashBalance FROM Account WHERE AccountID = {the applicable AccountID}) >= ABS({the amount to transfer}) THEN
INSERT INTO Transfer (AccountID, Amount, DateInitiated, DateCompleted)
VALUES ({the applicable AccountID}, {the amount to transfer}, {DateInitiated, set to CURRENT_DATE}, {DateCompleted, set to CURRENT_DATE for simplicity});

UPDATE Account
SET CashBalance = CashBalance + {the amount to transfer}
WHERE AccountID = {the applicable AccountID};
COMMIT;

ELSEIF {the amount to transfer} > 0 THEN
INSERT INTO Transfer (AccountID, Amount, DateInitiated, DateCompleted)
VALUES ({the applicable AccountID}, {the amount to transfer}, {DateInitiated, set to CURRENT_DATE}, {DateCompleted, set to CURRENT_DATE for simplicity});

UPDATE Account
SET CashBalance = CashBalance + {the amount to transfer}
WHERE AccountID = {the applicable AccountID};
COMMIT;

ELSE ROLLBACK;
END IF;

-- Query using sample values of AccountID = 1 and transfer amount of -100
BEGIN TRANSACTION;
-- Only check balance if the transfer is negative
IF -100 < 0 AND (SELECT CashBalance FROM Account WHERE AccountID = 1) >= ABS(-100) THEN
INSERT INTO Transfer (AccountID, Amount, DateInitiated, DateCompleted)
VALUES (1, -100, CURRENT_DATE, CURRENT_DATE);

UPDATE Account
SET CashBalance = CashBalance + (-100)
WHERE AccountID = 1;
COMMIT;

ELSEIF -100 > 0 THEN
INSERT INTO Transfer (AccountID, Amount, DateInitiated, DateCompleted)
VALUES (1, -100, CURRENT_DATE, CURRENT_DATE);

UPDATE Account
SET CashBalance = CashBalance + (-100)
WHERE AccountID = 1;
COMMIT;

ELSE ROLLBACK;
END IF;

-- *** BUY/SELL Transaction, Various Queries to Check for Constraints**********************************************
-- Note that we would need to implement rollback for the transaction if any of the constraints are violated

-- ***Gets Current Prices***
-- Get temporary table of security prices for today and check against ticker input by user if currency is USD
WITH TodayPrices AS (
    SELECT SecurityID, Price
    FROM SecurityPrice
    WHERE Date = CURRENT_DATE),
    SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security)

SELECT SecurityInfo.SecurityID, SecurityInfo.Ticker, SecurityInfo.Name, TodayPrices.Price
FROM SecurityInfo
LEFT JOIN TodayPrices ON SecurityInfo.SecurityID = TodayPrices.SecurityID
WHERE SecurityInfo.Ticker = { whatever Security ticker is input by user };

-- Get values of security and currency prices for today and check against ticker input by user if currency is non-USD
WITH

    TodayPrices AS (
    SELECT SecurityID, Price
    FROM SecurityPrice
    WHERE Date = CURRENT_DATE),

    SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
    WHERE Ticker = { whatever Security ticker is input by user }),

    CurrencyLookup AS (
    SELECT CurrencyID, CurrencyUSD_FXRate
    FROM CurrencyRate
    WHERE AsOfDate = CURRENT_DATE)

SELECT SecurityInfo.SecurityID, SecurityInfo.Ticker, SecurityInfo.Name, TodayPrices.Price
FROM SecurityInfo
LEFT JOIN TodayPrices ON SecurityInfo.SecurityID = TodayPrices.SecurityID
LEFT JOIN CurrencyLookup ON Security.CurrencyID = CurrencyLookup.CurrencyID
WHERE SecurityInfo.Ticker = { whatever Security ticker is input by user };

-- Test with AAPL and a date where the price is present (2023-01-03)
WITH

    TodayPrices AS (
    SELECT SecurityID, Price, Date
    FROM SecurityPrice
    WHERE Date = '2023-01-03'),

    SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security)

SELECT SecurityInfo.SecurityID, SecurityInfo.Ticker, SecurityInfo.Name, TodayPrices.Price, TodayPrices.Date
FROM SecurityInfo
LEFT JOIN TodayPrices ON SecurityInfo.SecurityID = TodayPrices.SecurityID
WHERE SecurityInfo.Ticker = 'NASDAQ:AAPL';

-- ***Check Account Cash Balance***
SELECT AccountID, AccountType, CashBalance
FROM Account
WHERE AccountID = { whatever Account ID is selected };

-- Test with AccountID = 1
SELECT AccountID, AccountType, CashBalance
FROM Account
WHERE AccountID = 1;


-- ***Check Account Holdings Security Balance***
WITH

    AccountHoldings AS (
    SELECT AccountID, SecurityID, ShareCount
    FROM Holding
    WHERE AccountID = { whatever Account ID is selected }),

    SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
    WHERE Ticker = { whatever Security ticker is input by user }),

    SummedHoldings AS (
    SELECT AccountID, SUM(ShareCount) AS TotalShareCount
    FROM AccountHoldings
    GROUP BY AccountID)

SELECT SummedHoldings.AccountID, SecurityInfo.Ticker, SecurityInfo.Name, SummedHoldings.TotalShareCount
FROM SummedHoldings
LEFT JOIN SecurityInfo ON SummedHoldings.AccountID = SecurityInfo.SecurityID;


-- Test with AccountID = 1 and ticker = 'SPY'
WITH

    AccountHoldings AS (
    SELECT AccountID, SecurityID, ShareCount
    FROM Holding
    WHERE AccountID = 1),

    SecurityInfo AS (
    SELECT SecurityID, Ticker, Name
    FROM Security
    WHERE Ticker = 'SPY'),

    SummedHoldings AS (
    SELECT AccountHoldings.AccountID, AccountHoldings.SecurityID, SUM(ShareCount) AS TotalShareCount
    FROM AccountHoldings
    GROUP BY AccountHoldings.AccountID, AccountHoldings.SecurityID)

SELECT SummedHoldings.AccountID, SecurityInfo.Ticker, SecurityInfo.Name, SummedHoldings.TotalShareCount
FROM SummedHoldings
LEFT JOIN SecurityInfo ON SummedHoldings.SecurityID = SecurityInfo.SecurityID;


**************************************************************************************************************
Two of the web pages that require the most interesting database operations are the the following:

Account Profile Page
This page has various functionality to allow a user to view their account profile information, as well as historical transfer and transaction activity, and the holdings in their accounts. To display information properly, we must filter for the specific user whose profile we're viewing so we use "WHERE" clauses. Then to display the account's holdings, we had to join the "account", "security", and "holding" tables together to properly display the correct acccount name (ex: 401K) and security (ex: Apple) rather than IDs. Furthermore, for the Transactions section, we also had to join the "account", "security", and "transaction" tables together to properly display the accout name and security similar to the Holdings section. Also, for the Transactions section, because "BUY" or "SELL" is stored as a boolean in our database, we used case statements such that "if value = TRUE, then display BUY", etc. For the Transfer section, we also joined the "account" and "transfer" tables together to properly reflect that account name.

Securities Page
This page displays historical prices for selected securities based on a user's selected ticker, most notably historical prices which are joined from the "securitiesprices" table as well as the security's high level information from the "security" table. The chart renders dynamically based on the data range selected. Note that our database only contains data starting 1/3/22. For data past 2/28/24, we used a data generation function up to 4/5/24 as described in our proposal, as pulling real historical prices is prohibitively expensive.

Other Notes
For the Trades page where the SQL queries are above, but where we did not implement the front end, we also join the "currencyrate" table so that we can lookup the proper exchange rate for non-USD traded securities.

For the Transfer Execution function where the SQL queries are above, but where we did not implement the front end we also use the commit/rollback functions because we must check the cash balance of the account, and if it's not sufficient to do a transfer out, we do not execute the transfer.

Note that our app heavily uses dynamic callbacks which adds significant functionality, which is used in particular to ensure we're only looking at information for a particular user for the Account Profile Page or particular security for the Securities Page. Here is a visual representation of our callbacks:

https://drive.google.com/file/d/1RTlFXZnkQA0e39AwcawT1_X49Mzf4j_w/view?usp=drive_link

Note that the link is only visible to users with LionMail.