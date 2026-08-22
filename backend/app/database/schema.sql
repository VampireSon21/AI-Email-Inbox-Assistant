PRAGMA foreign_keys = ON;

-- =========================================================
-- 1. GMAIL ACCOUNTS
-- =========================================================

CREATE TABLE IF NOT EXISTS gmail_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_address TEXT NOT NULL UNIQUE,
    encrypted_token TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);


-- =========================================================
-- 2. EMAIL THREADS
-- =========================================================

CREATE TABLE IF NOT EXISTS email_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_id INTEGER NOT NULL,

    gmail_thread_id TEXT NOT NULL,
    subject TEXT,
    participants TEXT,
    latest_message_at TEXT,

    UNIQUE (account_id, gmail_thread_id),

    FOREIGN KEY (account_id)
        REFERENCES gmail_accounts(id)
        ON DELETE CASCADE
);


-- =========================================================
-- 3. EMAILS
-- =========================================================

CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_id INTEGER NOT NULL,
    thread_id INTEGER NOT NULL,

    gmail_message_id TEXT NOT NULL,

    sender TEXT NOT NULL,
    recipients TEXT,
    subject TEXT,
    body_text TEXT,
    snippet TEXT,
    received_at TEXT,
    labels TEXT,

    UNIQUE (account_id, gmail_message_id),

    FOREIGN KEY (account_id)
        REFERENCES gmail_accounts(id)
        ON DELETE CASCADE,

    FOREIGN KEY (thread_id)
        REFERENCES email_threads(id)
        ON DELETE CASCADE
);


-- =========================================================
-- 4. EMAIL ANALYSES
-- =========================================================

CREATE TABLE IF NOT EXISTS email_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    thread_id INTEGER NOT NULL UNIQUE,

    priority TEXT NOT NULL,
    requires_reply INTEGER NOT NULL DEFAULT 0,

    summary TEXT,
    decisions TEXT,
    open_questions TEXT,
    suggested_next_action TEXT,

    analyzed_at TEXT NOT NULL,

    CHECK (
        priority IN ('urgent', 'high', 'normal', 'low')
    ),

    FOREIGN KEY (thread_id)
        REFERENCES email_threads(id)
        ON DELETE CASCADE
);


-- =========================================================
-- 5. TASKS
-- =========================================================

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    thread_id INTEGER NOT NULL,
    source_email_id INTEGER NOT NULL,

    title TEXT NOT NULL,
    owner TEXT,
    deadline TEXT,

    status TEXT NOT NULL DEFAULT 'open',

    confidence REAL NOT NULL,

    CHECK (
        status IN ('open', 'completed', 'dismissed')
    ),

    CHECK (
        confidence >= 0
        AND confidence <= 1
    ),

    FOREIGN KEY (thread_id)
        REFERENCES email_threads(id)
        ON DELETE CASCADE,

    FOREIGN KEY (source_email_id)
        REFERENCES emails(id)
        ON DELETE CASCADE
);


-- =========================================================
-- 6. REPLY DRAFTS
-- =========================================================

CREATE TABLE IF NOT EXISTS reply_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    thread_id INTEGER NOT NULL,

    tone TEXT,
    content TEXT NOT NULL,

    is_selected INTEGER NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL,

    FOREIGN KEY (thread_id)
        REFERENCES email_threads(id)
        ON DELETE CASCADE
);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_threads_account
ON email_threads(account_id);

CREATE INDEX IF NOT EXISTS idx_emails_account
ON emails(account_id);

CREATE INDEX IF NOT EXISTS idx_emails_thread
ON emails(thread_id);

CREATE INDEX IF NOT EXISTS idx_emails_received
ON emails(received_at);

CREATE INDEX IF NOT EXISTS idx_tasks_thread
ON tasks(thread_id);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);

CREATE INDEX IF NOT EXISTS idx_drafts_thread
ON reply_drafts(thread_id);