CREATE TABLE systems (
    id SERIAL PRIMARY KEY,                  -- Unique ID
    hostname TEXT,                          -- System hostname
    os TEXT,                                -- Operating system
    cpu TEXT,                               -- CPU info
    ram TEXT,                               -- RAM info
    ip_address TEXT,                        -- IP address
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Last contact time
);

CREATE TABLE software (
    id SERIAL PRIMARY KEY,                  -- Unique ID
    system_id INTEGER REFERENCES systems(id) ON DELETE CASCADE,  -- Link to system
    name TEXT,                              -- Software name
    version TEXT,                           -- Version
    installed_on DATE                       -- Install date
);
