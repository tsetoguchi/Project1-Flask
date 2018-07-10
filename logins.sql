CREATE TABLE logins (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    zipcode INTEGER REFERENCES zips
);