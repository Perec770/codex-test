diff --git a//dev/null b/good-deeds-bot/keyboards.py
index 0000000000000000000000000000000000000000..9685f9cd9a5fd7fdae63370e67dc2e964c337598 100644
--- a//dev/null
+++ b/good-deeds-bot/keyboards.py
@@ -0,0 +1,32 @@
+from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
+from aiogram import types
+
+
+MAIN_BUTTONS = [
+    "\u2795 Отметить",
+    "\ud83c\udf81 Идеи",
+    "\ud83d\udcca Прогресс",
+    "\u2699\ufe0f Настройки",
+]
+
+PRESET_ACTIONS = [
+    "Помощь по дому",
+    "Доброе слово",
+    "Поделиться игрушкой",
+]
+
+def main_menu() -> types.ReplyKeyboardMarkup:
+    kb = ReplyKeyboardBuilder()
+    for btn in MAIN_BUTTONS:
+        kb.button(text=btn)
+    kb.adjust(2)
+    return kb.as_markup(resize_keyboard=True)
+
+
+def mark_actions_kb() -> types.InlineKeyboardMarkup:
+    kb = InlineKeyboardBuilder()
+    for action in PRESET_ACTIONS:
+        kb.button(text=action, callback_data=f"preset:{action}")
+    kb.button(text="Свой вариант", callback_data="custom")
+    kb.adjust(1)
+    return kb.as_markup()
