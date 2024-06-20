import sqlite3
import time

if __name__ == "__main__":
    filepath = "./test.db"

    conn = sqlite3.connect(filepath)
    cur = conn.cursor()

    print("Database tables:")
    for r in cur.execute("select * from sqlite_master"):
        print(r)

    # Get rows where the usernames match
    start = time.time()
    usernames = ["A", "B"]
    res = cur.execute(
        "select * from users where username in (%s)" % ",".join("?" * len(usernames)),
        usernames,
    )
    res.fetchall()
    print(f"Time taken: {time.time() - start} seconds")

    res = cur.execute(
        "explain query plan select * from users where username in (%s)"
        % ",".join("?" * len(usernames)),
        usernames,
    )
    print(res.fetchall())

    res = cur.execute(
        "select * from users indexed by idx_user_username where username in (%s)"
        % ",".join("?" * len(usernames)),
        usernames,
    )
    print(res.fetchone())
