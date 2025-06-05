diff --git a//dev/null b/good-deeds-bot/database.py
index 0000000000000000000000000000000000000000..ab2a854461b0d6ca516a74d27c81823501696a5e 100644
--- a//dev/null
+++ b/good-deeds-bot/database.py
@@ -0,0 +1,88 @@
+import os
+import sqlite3
+from datetime import datetime
+
+class Database:
+    def __init__(self, path: str = "gooddeeds.db"):
+        self.path = path
+        self.conn = sqlite3.connect(self.path, check_same_thread=False)
+        self.conn.row_factory = sqlite3.Row
+        self.create_tables()
+
+    def create_tables(self):
+        cur = self.conn.cursor()
+        cur.execute(
+            """CREATE TABLE IF NOT EXISTS users (
+            tg_id INTEGER PRIMARY KEY,
+            first_name TEXT,
+            last_name TEXT
+        )"""
+        )
+        cur.execute(
+            """CREATE TABLE IF NOT EXISTS children (
+            id INTEGER PRIMARY KEY AUTOINCREMENT,
+            user_id INTEGER,
+            name TEXT
+        )"""
+        )
+        cur.execute(
+            """CREATE TABLE IF NOT EXISTS actions (
+            id INTEGER PRIMARY KEY AUTOINCREMENT,
+            child_id INTEGER,
+            timestamp TEXT
+        )"""
+        )
+        self.conn.commit()
+
+    def add_user(self, tg_id: int, first_name: str = "", last_name: str = ""):
+        with self.conn:
+            self.conn.execute(
+                "INSERT OR IGNORE INTO users(tg_id, first_name, last_name) VALUES(?,?,?)",
+                (tg_id, first_name, last_name),
+            )
+
+    def get_user(self, tg_id: int):
+        cur = self.conn.cursor()
+        cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
+        return cur.fetchone()
+
+    def add_child(self, user_id: int, name: str) -> int:
+        with self.conn:
+            cur = self.conn.execute(
+                "INSERT INTO children(user_id, name) VALUES(?, ?)",
+                (user_id, name),
+            )
+        return cur.lastrowid
+
+    def get_children(self, user_id: int):
+        cur = self.conn.cursor()
+        cur.execute("SELECT * FROM children WHERE user_id=?", (user_id,))
+        return cur.fetchall()
+
+    def add_action(self, child_id: int):
+        with self.conn:
+            self.conn.execute(
+                "INSERT INTO actions(child_id, timestamp) VALUES(?, ?)",
+                (child_id, datetime.utcnow().isoformat()),
+            )
+
+    def get_total_actions(self, child_id: int) -> int:
+        cur = self.conn.cursor()
+        cur.execute("SELECT COUNT(*) FROM actions WHERE child_id=?", (child_id,))
+        row = cur.fetchone()
+        return row[0] if row else 0
+
+    def get_last_actions(self, child_id: int, limit: int = 5):
+        cur = self.conn.cursor()
+        cur.execute(
+            "SELECT timestamp FROM actions WHERE child_id=? ORDER BY id DESC LIMIT ?",
+            (child_id, limit),
+        )
+        return [row[0] for row in cur.fetchall()]
+
+    def get_or_create_default_child(self, user_id: int) -> int:
+        children = self.get_children(user_id)
+        if children:
+            return children[0]["id"]
+        return self.add_child(user_id, "Child")
+
