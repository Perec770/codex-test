diff --git a//dev/null b/good-deeds-bot/gift_ideas.py
index 0000000000000000000000000000000000000000..044008211d3503ea2644a984313f59fc3d4f6f50 100644
--- a//dev/null
+++ b/good-deeds-bot/gift_ideas.py
@@ -0,0 +1,22 @@
+import os
+from openai import AsyncOpenAI
+
+STATIC_IDEAS = [
+    "\U0001F3A8 Набор для творчества",
+    "\U0001F4DA Новая книга",
+    "\U0001F3AE Настольная игра",
+]
+
+async def ai_ideas(age: int, interests: list[str], budget: int) -> list[str]:
+    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
+    prompt = (
+        "Предложи 3 идеи подарков для ребёнка {age} лет. "
+        "Интересы: {interests}. Бюджет: до {budget} рублей."
+    ).format(age=age, interests=", ".join(interests), budget=budget)
+    response = await client.chat.completions.create(
+        model="gpt-4o",
+        messages=[{"role": "user", "content": prompt}],
+        n=1,
+    )
+    text = response.choices[0].message.content
+    return [item.strip() for item in text.split("\n") if item.strip()][:3]
