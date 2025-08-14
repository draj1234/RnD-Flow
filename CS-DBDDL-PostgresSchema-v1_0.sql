-- CS-DBDDL-PostgresSchema-v1_0.sql
-- Project: ClearSight – Production Traceability System
-- Persona: Solutions Architect
-- Version: v1.0
-- Date: 2025-08-10

CREATE TABLE sku_master (
    sku_id SERIAL PRIMARY KEY,
    sku_code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    erp_reference VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE boards (
    board_id SERIAL PRIMARY KEY,
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    sku_id INT REFERENCES sku_master(sku_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE stages (
    stage_id SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) UNIQUE NOT NULL,
    sequence_order INT NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(50) NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE stage_events (
    event_id SERIAL PRIMARY KEY,
    board_id INT REFERENCES boards(board_id),
    stage_id INT REFERENCES stages(stage_id),
    user_id INT REFERENCES users(user_id),
    action VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE erp_sync_logs (
    sync_id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    details TEXT,
    synced_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_boards_serial ON boards(serial_number);
CREATE INDEX idx_stage_events_board ON stage_events(board_id);
CREATE INDEX idx_stage_events_stage ON stage_events(stage_id);
