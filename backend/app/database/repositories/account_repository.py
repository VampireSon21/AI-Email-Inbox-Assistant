class AccountRepository:

    def __init__(self, connection):
        self.connection = connection

    def save_account(
        self,
        email_address,
        encrypted_token,
        created_at,
        updated_at
    ):
        cursor = self.connection.execute(
            """
            INSERT INTO gmail_accounts
            (
                email_address,
                encrypted_token,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                email_address,
                encrypted_token,
                created_at,
                updated_at
            )
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_account(self, account_id):
        return self.connection.execute(
            """
            SELECT *
            FROM gmail_accounts
            WHERE id = ?
            """,
            (account_id,)
        ).fetchone()

    def list_accounts(self):
        return self.connection.execute(
            """
            SELECT *
            FROM gmail_accounts
            ORDER BY id DESC
            """
        ).fetchall()

    def delete_account(self, account_id):
        self.connection.execute(
            """
            DELETE FROM gmail_accounts
            WHERE id = ?
            """,
            (account_id,)
        )

        self.connection.commit()