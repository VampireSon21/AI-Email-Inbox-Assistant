class AnalysisRepository:

    def __init__(self, connection):
        self.connection = connection

    def save_analysis(
        self,
        thread_id,
        priority,
        requires_reply,
        summary,
        decisions,
        open_questions,
        suggested_next_action,
        analyzed_at
    ):
        existing = self.connection.execute(
            """
            SELECT id
            FROM email_analyses
            WHERE thread_id = ?
            """,
            (thread_id,)
        ).fetchone()

        if existing:
            self.connection.execute(
                """
                UPDATE email_analyses
                SET priority = ?,
                    requires_reply = ?,
                    summary = ?,
                    decisions = ?,
                    open_questions = ?,
                    suggested_next_action = ?,
                    analyzed_at = ?
                WHERE thread_id = ?
                """,
                (
                    priority,
                    requires_reply,
                    summary,
                    decisions,
                    open_questions,
                    suggested_next_action,
                    analyzed_at,
                    thread_id
                )
            )

            self.connection.commit()
            return existing["id"]

        cursor = self.connection.execute(
            """
            INSERT INTO email_analyses
            (
                thread_id,
                priority,
                requires_reply,
                summary,
                decisions,
                open_questions,
                suggested_next_action,
                analyzed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                thread_id,
                priority,
                requires_reply,
                summary,
                decisions,
                open_questions,
                suggested_next_action,
                analyzed_at
            )
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_analysis_by_thread_id(self, thread_id):
        return self.connection.execute(
            """
            SELECT *
            FROM email_analyses
            WHERE thread_id = ?
            """,
            (thread_id,)
        ).fetchone()