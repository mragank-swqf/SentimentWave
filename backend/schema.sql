CREATE TABLE transcripts (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    quarter SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    raw_text TEXT NOT NULL,
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    transcript_id INTEGER REFERENCES transcripts(id),
    segment_index SMALLINT NOT NULL,
    speaker VARCHAR(100),
    role VARCHAR(50),
    text TEXT NOT NULL,
    topic_label VARCHAR(255),
    sentiment_score FLOAT,
    tone VARCHAR(50),
    hedging_phrases JSONB DEFAULT '[]'
);

CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    transcript_id INTEGER REFERENCES transcripts(id),
    overall_sentiment FLOAT,
    summary TEXT,
    notable_moments JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);