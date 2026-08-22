class TaskRepository:

    def __init__(self, connection):
        self.connection = connection

    def save_tasks(self, tasks):
        saved_ids = []

        for task in tasks:
            cursor = self.connection.execute(
                """
                INSERT INTO tasks
                (
                    thread_id,
                    source_email_id,
                    title,
                    owner,
                    deadline,
                    status,
                    confidence
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task["thread_id"],
                    task["source_email_id"],
                    task["title"],
                    task.get("owner"),
                    task.get("deadline"),
                    task.get("status", "open"),
                    task["confidence"]
                )
            )

            saved_ids.append(cursor.lastrowid)

        self.connection.commit()

        return saved_ids

    def list_tasks(self, thread_id=None, status=None):
        query = """
            SELECT *
            FROM tasks
            WHERE 1 = 1
        """

        params = []

        if thread_id is not None:
            query += " AND thread_id = ?"
            params.append(thread_id)

        if status is not None:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY deadline ASC"

        return self.connection.execute(
            query,
            params
        ).fetchall()

    def update_task_status(self, task_id, status):
        self.connection.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,
            (status, task_id)
        )

        self.connection.commit()