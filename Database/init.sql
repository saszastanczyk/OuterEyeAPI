CREATE DATABASE outer_eye_db;

\c outer_eye_db;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY ,
    username VARCHAR(100) NOT NULL,
    karma INTEGER DEFAULT 20,
    register_date DATE DEFAULT NOW()
);

CREATE TABLE positions(
    position_id SERIAL PRIMARY KEY,
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL,
    pos_z INTEGER NOT NULL
);

CREATE TABLE actions(
    action_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
    position_id INTEGER REFERENCES positions(position_id) NOT NULL,
    happen_time TIMESTAMP DEFAULT NOW()

);

CREATE TABLE meal_actions(
    meal_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE NOT NULL,
    meal_name VARCHAR(100) NOT NULL
);

CREATE TABLE craft_actions(
    craft_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE NOT NULL,
    craft_subject VARCHAR(100) NOT NULL,
    amount INTEGER DEFAULT 1
);

CREATE TABLE kill_actions(
    kill_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE NOT NULL,
    killed_type VARCHAR(100) NOT NULL,
    killed_subject_id UUID NOT NULL,
    kill_TOOL VARCHAR(100)
);

CREATE TABLE breed_actions(
    breed_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE NOT NULL,
    father_subject_id UUID NOT NULL,
    mother_subject_id UUID NOT NULL,
    child_subject_id UUID NOT NULL
);

CREATE TABLE death_actions(
    death_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE,
    death_cause TEXT
);

CREATE TABLE pray_actions(
    pray_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES actions(action_id) ON DELETE CASCADE NOT NULL,
    pray_text TEXT,
    pray_respond TEXT
);

CREATE TABLE inventory_scans(
    inventory_scan_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
    time TIMESTAMP
);

CREATE TABLE inventory_scan_items(
    scan_item_id SERIAL PRIMARY KEY,
    inventory_scan_id INTEGER REFERENCES inventory_scans(inventory_scan_id) ON DELETE CASCADE NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    amount INTEGER NOT NULL
);

CREATE TABLE positions_scans(
    position_scan_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE NOT NULL,
    position_id INTEGER REFERENCES positions(position_id) ON DELETE CASCADE NOT NULL,
    scan_time TIMESTAMP DEFAULT NOW()
);

CREATE INDEX actions_user_idx ON actions(user_id);
CREATE INDEX actions_date_idx ON actions(happen_time DESC);
CREATE INDEX meal_action_idx ON meal_actions(action_id);
CREATE INDEX craft_action_idx ON craft_actions(action_id);
CREATE INDEX kill_action_idx ON kill_actions(action_id);
CREATE INDEX death_action_idx ON death_actions(action_id);
CREATE INDEX pray_action ON pray_actions(action_id);
CREATE INDEX inventory_scan_user ON inventory_scans(inventory_scan_id);
CREATE INDEX inventory_scan_time ON inventory_scans(time DESC);
CREATE INDEX inventory_scan_item_scan ON inventory_scan_items(inventory_scan_id);
CREATE INDEX positions_scan_user ON positions_scans(user_id);
CREATE INDEX positions_scan_time ON positions_scans(scan_time DESC);