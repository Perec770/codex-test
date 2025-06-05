diff --git a//dev/null b/good-deeds-bot/rewards.py
index 0000000000000000000000000000000000000000..767cc75bfb89f0ff0d1171e259587cf1d36fbb99 100644
--- a//dev/null
+++ b/good-deeds-bot/rewards.py
@@ -0,0 +1,4 @@
+from .texts import REWARD_THRESHOLDS
+
+def check_rewards(total: int):
+    return REWARD_THRESHOLDS.get(total)
