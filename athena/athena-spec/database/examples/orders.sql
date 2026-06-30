CREATE TABLE orders (
 id UUID PRIMARY KEY,
 symbol VARCHAR(32),
 status VARCHAR(20),
 created_at TIMESTAMP
);
