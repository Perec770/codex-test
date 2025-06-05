diff --git a//dev/null b/good-deeds-bot/scheduler.py
index 0000000000000000000000000000000000000000..bf15186d84755b29d338ad808cc44b83576b4c6a 100644
--- a//dev/null
+++ b/good-deeds-bot/scheduler.py
@@ -0,0 +1,17 @@
+from apscheduler.schedulers.asyncio import AsyncIOScheduler
+from aiogram import Bot
+from datetime import time
+
+
+class ReminderScheduler:
+    def __init__(self, bot: Bot):
+        self.bot = bot
+        self.scheduler = AsyncIOScheduler()
+
+    async def send_reminders(self):
+        # placeholder: should iterate over users and send messages
+        pass
+
+    def start(self):
+        self.scheduler.add_job(self.send_reminders, 'cron', hour=20)
+        self.scheduler.start()
