-- Run in a fresh PostgreSQL database named retail_behavior.
-- These event tables deliberately have no uniqueness constraint.
CREATE TABLE purchase_events (
    client_id BIGINT NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    sku BIGINT NOT NULL
);
CREATE TABLE cart_events (
    client_id BIGINT NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    sku BIGINT NOT NULL
);
