class ThreadRepository:

    def __init__(self, connection):
        self.connection = connection

    def upsert_thread(
        self,
        account_id,
        gmail_thread_id,
        subject,
        participants,
        latest_message_at
    ):
        existing = self.connection.execute(
            """
            SELECT id
            FROM email_threads
            WHERE account_id = ?
              AND gmail_thread_id = ?
            """,
            (account_id, gmail_thread_id)
        ).fetchone()

        if existing:
            self.connection.execute(
                """
                UPDATE email_threads
                SET subject = ?,
                    participants = ?,
                    latest_message_at = ?
                WHERE id = ?
                """,
                (
                    subject,
                    participants,
                    latest_message_at,
                    existing["id"]
                )
            )

            self.connection.commit()
            return existing["id"]

        cursor = self.connection.execute(
            """
            INSERT INTO email_threads
            (
                account_id,
                gmail_thread_id,
                subject,
                participants,
                latest_message_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                account_id,
                gmail_thread_id,
                subject,
                participants,
                latest_message_at
            )
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_thread(self, thread_id):
        return self.connection.execute(
            """
            SELECT *
            FROM email_threads
            WHERE id = ?
            """,
            (thread_id,)
        ).fetchone()

    def list_threads(self, account_id):
        return self.connection.execute(
            """
            SELECT *
            FROM email_threads
            WHERE account_id = ?
            ORDER BY latest_message_at DESC
            """,
            (account_id,)
        ).fetchall()