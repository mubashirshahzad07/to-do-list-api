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
    INSERT INTO users (username, email, password_hash)
    VALUES(?, ?, ?)
"""

find_user_with_email = """
    SELECT id, password_hash
    FROM users
    WHERE email = ?
"""

add_todo_item = """
    INSERT INTO todos (user_id, title, description)
    VALUE(?, ?, ?)
"""

get_todo_items_count = """
    SELECT COUNT(*) 
    FROM todos 
    WHERE user_id = ?
"""

get_updated_todo_item_index = """
    SELECT COUNT(*) 
    FROM todos 
    WHERE user_id = ? and id <= ?;
"""

update_todo_item = """
    UPDATE todos
    SET title = ?, description = ?
    WHERE id = ?
"""

get_todo_item = """
    SELECT user_id
    FROM todos
    WHERE id = ? 
"""