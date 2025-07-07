CREATE TABLE user_details (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(120) UNIQUE,
    password VARCHAR(128)
);

CREATE TABLE snippet (
    id SERIAL PRIMARY KEY,
    code TEXT,
    language VARCHAR(50),
    explanation TEXT,
    user_id INTEGER REFERENCES user_details(id)
);

CREATE TABLE challenge (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    difficulty VARCHAR(20),
    test_case TEXT
);
