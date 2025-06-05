diff --git a//dev/null b/good-deeds-bot/bot.py
index 0000000000000000000000000000000000000000..6d74f5a577a39069d5382258f818af9a0e34a388 100644
--- a//dev/null
+++ b/good-deeds-bot/bot.py
@@ -0,0 +1,72 @@
+import os
+import random
+from aiogram import Bot, Dispatcher, types
+from aiogram.filters import Command, Text
+from aiogram.types import CallbackQuery
+from dotenv import load_dotenv
+
+from database import Database
+from keyboards import main_menu, mark_actions_kb
+from texts import PRAISES
+from rewards import check_rewards
+
+load_dotenv()
+
+BOT_TOKEN = os.getenv("BOT_TOKEN")
+
+db = Database()
+
+bot = Bot(BOT_TOKEN)
+dp = Dispatcher()
+
+
+def get_child_id(user_id: int) -> int:
+    return db.get_or_create_default_child(user_id)
+
+
+@dp.message(Command("start"))
+async def cmd_start(message: types.Message):
+    db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name or "")
+    child_id = get_child_id(message.from_user.id)
+    await message.answer(
+        "Добро пожаловать в Добрые баллы!", reply_markup=main_menu()
+    )
+
+
+@dp.message(Text("\u2795 Отметить"))
+async def mark_action(message: types.Message):
+    await message.answer("Выберите действие:", reply_markup=mark_actions_kb())
+
+
+@dp.callback_query(Text(startswith="preset:"))
+async def preset_chosen(callback: CallbackQuery):
+    user_id = callback.from_user.id
+    child_id = get_child_id(user_id)
+    db.add_action(child_id)
+    total = db.get_total_actions(child_id)
+    await callback.answer(random.choice(PRAISES), show_alert=True)
+    reward = check_rewards(total)
+    if reward:
+        with open(os.path.join(os.path.dirname(__file__), "assets", "reward.png"), "rb") as img:
+            await callback.message.answer_photo(img, caption=reward)
+    await callback.message.edit_reply_markup(reply_markup=None)
+
+
+@dp.message(Text("\ud83d\udcca Прогресс"))
+async def progress(message: types.Message):
+    user_id = message.from_user.id
+    child_id = get_child_id(user_id)
+    total = db.get_total_actions(child_id)
+    last = db.get_last_actions(child_id)
+    text = f"Всего баллов: {total}\nПоследние поступки:\n" + "\n".join(last)
+    await message.answer(text)
+
+
+async def main():
+    await dp.start_polling(bot)
+
+
+if __name__ == "__main__":
+    import asyncio
+    asyncio.run(main())
+
