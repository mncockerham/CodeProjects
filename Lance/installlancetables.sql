INSTALL lance;

LOAD lance;

-- DBeaver usually needs absolute paths if the ~ doesn't resolve correctly
CREATE VIEW sample_users AS
SELECT
    *
FROM
    '/Users/mark/LocalData/Lance/sample_users.lance';

-- Now you can query it like a normal table!
SELECT
    *
FROM
    sample_users
LIMIT
    20;

SELECT
    count(1)
FROM
    sample_users