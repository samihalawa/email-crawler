-- Create the leadsgood table
CREATE TABLE leadsgood (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) NOT NULL,
    lead_source VARCHAR(255),
    url TEXT,
    page_title TEXT,
    meta_description TEXT,
    scrape_duration INTERVAL,
    http_status INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_term VARCHAR(255)
);

-- Create indexes for better performance on the leadsgood table
CREATE INDEX idx_email ON leadsgood (email);
CREATE INDEX idx_created_at ON leadsgood (created_at);
CREATE INDEX idx_search_term ON leadsgood (search_term);

-- Create the campaigns table
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    search_query TEXT NOT NULL,
    email_template TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Create the search_queries table for storing search queries
CREATE TABLE search_queries (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    total_contacts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the emails table for storing email content
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    search_query_id INTEGER REFERENCES search_queries(id),
    email VARCHAR(254) NOT NULL,
    page_title TEXT,
    url TEXT,
    meta_description TEXT
);

-- Create indexes for better performance on the campaigns table
CREATE INDEX idx_campaign_name ON campaigns (name);
CREATE INDEX idx_created_at_campaigns ON campaigns (created_at);

-- Create indexes for better performance on the search_queries table
CREATE INDEX idx_query ON search_queries (query);
CREATE INDEX idx_created_at_search_queries ON search_queries (created_at);