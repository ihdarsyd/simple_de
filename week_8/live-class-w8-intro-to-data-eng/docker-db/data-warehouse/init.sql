CREATE TABLE IF NOT EXISTS hotel_analysis_table(
    analysis_id SERIAL NOT NULL PRIMARY KEY,
    reservation_id integer,
    full_name varchar,
    email varchar,
    domain_email varchar,
    reservation_date timestamp,
    payment_date varchar,
    start_date timestamp,
    end_date timestamp,
    total_price numeric,
    currency varchar,
    provider varchar,
    payment_status varchar,
    created_at timestamp NOT NULL DEFAULT NOW()
);