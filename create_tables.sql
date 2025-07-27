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
    title VARCHAR(128) NOT NULL,
    description TEXT NOT NULL,
    starter_code_python TEXT NOT NULL,
    starter_code_cpp TEXT,
    starter_code_java TEXT,
    starter_code_javascript TEXT,
    starter_code_csharp TEXT,
    test_cases TEXT NOT NULL, -- Store as JSON string
    difficulty VARCHAR(32) NOT NULL
);

CREATE TABLE user_challenge_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_details(id),
    challenge_id INTEGER NOT NULL REFERENCES challenge(id),
    attempts INTEGER DEFAULT 0,
    solved BOOLEAN DEFAULT FALSE,
    last_code TEXT,
    last_feedback TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Ensure a user can only have one progress record per challenge
ALTER TABLE user_challenge_progress
ADD CONSTRAINT unique_user_challenge UNIQUE (user_id, challenge_id);
ALTER TABLE user_details ADD COLUMN preferences TEXT;