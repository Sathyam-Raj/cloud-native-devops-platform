CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    product VARCHAR(100) NOT NULL
);

INSERT INTO users (name)
VALUES
    ('Alice'),
    ('Bob'),
    ('Charlie')
ON CONFLICT DO NOTHING;

INSERT INTO orders (user_id, product)
VALUES
    (1, 'Laptop'),
    (2, 'Keyboard'),
    (3, 'Monitor')
ON CONFLICT DO NOTHING;