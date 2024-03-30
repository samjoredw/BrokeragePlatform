
-- ***Profile Page***************************************************************************************************
-- ***User Name (Menu Pulldown)*** ----------------------------------------------------------------------------------------------------------
SELECT FirstName || LastName AS FullName
FROM "user"
ORDER BY FullName;

-- ***Profile*** ----------------------------------------------------------------------------------------------------------------------------
SELECT FirstName, LastName, DateOfBirth, StreetAddress, City, Zip, Country, PhoneNumber, BankAccountRouting, BankAccountNumber
FROM "user"
WHERE UserID = { whatever User ID is selected };

-- Test where UserID = 1
SELECT FirstName, LastName, DateOfBirth, StreetAddress, City, Zip, Country, PhoneNumber, BankAccountRouting, BankAccountNumber
FROM "user"
WHERE UserID = 1;

-- Alternatively, we can just do a SELECT * and choose the columns we want to display in the application
SELECT *
FROM "user"
WHERE UserID = 1;

-- ***Accounts*** --------------------------------------------------------------
-- <<MISSING YTD% CHANGE RIGHT NOW>>
SELECT AccountType, CreationDate, AccountStatus, CashBalance
FROM Account
WHERE UserID = { whatever User ID is selected }
ORDER BY CreationDate;

-- ***Holdings***
-- <<SIMPLE VERSION, DOES NOT HAVE CALCS JUST LISTS HOLDINGS FOR NOW>>
WITH AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = { whatever User ID is selected }
), SecurityInfo AS (
    SELECT SecurityID, Name
    FROM Security
)

SELECT AccountTypes.AccountType, SecurityInfo.Name, Holding.ShareCount, Holding.PurchasePrice, Holding.PurchaseDate
FROM Holding
LEFT JOIN AccountTypes ON Holding.AccountID = AccountTypes.AccountID
LEFT JOIN SecurityInfo ON Holding.SecurityID = SecurityInfo.SecurityID
WHERE Holding.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = { whatever User ID is selected }
);

-- Holdings Test with UserID = 1
WITH AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = 1
), SecurityInfo AS (
    SELECT SecurityID, Name
    FROM Security
)

SELECT AccountTypes.AccountType, SecurityInfo.Name, Holding.ShareCount, Holding.PurchasePrice, Holding.PurchaseDate
FROM Holding
LEFT JOIN AccountTypes ON Holding.AccountID = AccountTypes.AccountID
LEFT JOIN SecurityInfo ON Holding.SecurityID = SecurityInfo.SecurityID
WHERE Holding.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = 1
);

-- ***Transactions*** ----------------------------------------------------------------------------------------------------------------------

WITH AccountInfo AS (
    SELECT TransactionID, SecurityID, ShareCount, Price, Action, DateInitiated, DateCompleted, AccountID
    FROM Transaction
    WHERE AccountID IN (
        SELECT AccountID
        FROM Account
        WHERE UserID = { whatever User ID is selected }
    )
), AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = { whatever User ID is selected }
), SecurityInfo AS (
    SELECT SecurityID, Name
    FROM Security
)

SELECT AccountTypes.AccountType, AccountInfo.AccountID, AccountInfo.TransactionID, AccountInfo.SecurityID, SecurityInfo.Name, AccountInfo.ShareCount, AccountInfo.Price,
    CASE WHEN AccountInfo.Action = true THEN 'BUY'
    WHEN AccountInfo.Action = false THEN 'SELL'
END AS BuySell, AccountInfo.DateInitiated, AccountInfo.DateCompleted
FROM AccountInfo
LEFT JOIN AccountTypes ON AccountInfo.AccountID = AccountTypes.AccountID
LEFT JOIN SecurityInfo ON AccountInfo.SecurityID = SecurityInfo.SecurityID
WHERE AccountInfo.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = { whatever User ID is selected }
)
ORDER BY AccountInfo.DateCompleted DESC;

-- Transaction Test with UserID = 1
WITH AccountInfo AS (
    SELECT TransactionID, SecurityID, ShareCount, Price, Action, DateInitiated, DateCompleted, AccountID
    FROM Transaction
    WHERE AccountID IN (
        SELECT AccountID
        FROM Account
        WHERE UserID = 1
    )
), AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = 1
), SecurityInfo AS (
    SELECT SecurityID, Name
    FROM Security
)

SELECT AccountTypes.AccountType, AccountInfo.AccountID, AccountInfo.TransactionID, AccountInfo.SecurityID, SecurityInfo.Name, AccountInfo.ShareCount, AccountInfo.Price,
    CASE WHEN AccountInfo.Action = true THEN 'BUY'
    WHEN AccountInfo.Action = false THEN 'SELL'
END AS BuySell, AccountInfo.DateInitiated, AccountInfo.DateCompleted
FROM AccountInfo
LEFT JOIN AccountTypes ON AccountInfo.AccountID = AccountTypes.AccountID
LEFT JOIN SecurityInfo ON AccountInfo.SecurityID = SecurityInfo.SecurityID
WHERE AccountInfo.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = 1
)
ORDER BY AccountInfo.DateCompleted DESC;


-- ***Transfers*** ----------------------------------------------------------------------------------------------------------------------------
WITH AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = { whatever User ID is selected }
)

SELECT AccountTypes.AccountType, TransferID, Amount, DateInitiated, DateCompleted
FROM Transfer
LEFT JOIN AccountTypes ON Transfer.AccountID = AccountTypes.AccountID
WHERE Transfer.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = { whatever User ID is selected }
)
ORDER BY DateCompleted DESC;

-- Transfer Test with UserID = 1
WITH AccountTypes AS (
    SELECT AccountID, AccountType
    FROM Account
    WHERE UserID = 1
)

SELECT AccountTypes.AccountType, TransferID, Amount, DateInitiated, DateCompleted
FROM Transfer
LEFT JOIN AccountTypes ON Transfer.AccountID = AccountTypes.AccountID
WHERE Transfer.AccountID IN (
    SELECT AccountID
    FROM Account
    WHERE UserID = 1
)
ORDER BY DateCompleted DESC;


-- *** Name Lookup by AccountID *** ----------------------------------------------------------------------------------------------------------
SELECT "user".FirstName, "user".LastName, Account.AccountID, Account.AccountType, "user".FirstName || "user".LastName AS FullName
FROM "user"
LEFT JOIN Account ON "user".UserID = Account.UserID
WHERE Account.AccountID = { whatever Account ID is selected };

-- Test with AccountID = 1
SELECT "user".FirstName, "user".LastName, Account.AccountID, Account.AccountType, "user".FirstName || "user".LastName AS FullName
FROM "user"
LEFT JOIN Account ON "user".UserID = Account.UserID
WHERE Account.AccountID = 1;
