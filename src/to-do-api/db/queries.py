create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
"""

create_todos_table = """
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""

find_username_or_email = """
    SELECT id
    FROM users
    WHERE username = ? or email = ?
"""

add_user = """
    INSERT INTO uses (username, email, password_hash)
    VALUES(?, ?, ?)
"""