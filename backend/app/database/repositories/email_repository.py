class EmailRepository:

    def __init__(self, connection):
        self.connection = connection

    def save_email(
        self,
        account_id,
        thread_id,
        gmail_message_id,
        sender,
        recipients,
        subject,
        body_text,
        snippet,
        received_at,
        labels
    ):
        existing = self.connection.execute(
            """
            SELECT id
            FROM emails
            WHERE account_id = ?
              AND gmail_message_id = ?
            """,
            (account_id, gmail_message_id)
        ).fetchone()

        if existing:
            self.connection.execute(
                """
                UPDATE emails
                SET thread_id = ?,
                    sender = ?,
                    recipients = ?,
                    subject = ?,
                    body_text = ?,
                    snippet = ?,
                    received_at = ?,
                    labels = ?
                WHERE id = ?
                """,
                (
                    thread_id,
                    sender,
                    recipients,
                    subject,
                    body_text,
                    snippet,
                    received_at,
                    labels,
                    existing["id"]
                )
            )

            self.connection.commit()
            return existing["id"]

        cursor = self.connection.execute(
            """
            INSERT INTO emails
            (
                account_id,
                thread_id,
                gmail_message_id,
                sender,
                recipients,
                subject,
                body_text,
                snippet,
                received_at,
                labels
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                account_id,
                thread_id,
                gmail_message_id,
                sender,
                recipients,
                subject,
                body_text,
                snippet,
                received_at,
                labels
            )
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_email(self, email_id):
        return self.connection.execute(
            """
            SELECT *
            FROM emails
            WHERE id = ?
            """,
            (email_id,)
        ).fetchone()

    def list_recent_emails(self, account_id, limit=20):
        return self.connection.execute(
            """
            SELECT *
            FROM emails
            WHERE account_id = ?
            ORDER BY received_at DESC
            LIMIT ?
            """,
            (account_id, limit)
        ).fetchall()

    def search_emails(self, account_id, keyword):
        pattern = f"%{keyword}%"

        return self.connection.execute(
            """
            SELECT *
            FROM emails
            WHERE account_id = ?
              AND (
                    sender LIKE ?
                    OR subject LIKE ?
                    OR body_text LIKE ?
                  )
            ORDER BY received_at DESC
            """,
            (
                account_id,
                pattern,
                pattern,
                pattern
            )
        ).fetchall()