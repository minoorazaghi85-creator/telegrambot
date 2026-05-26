# test_env.py
import os
import sys

print("--- Starting Environment Test ---")
bot_token = os.getenv("Your token was replaced with a new one. You can use this token to access HTTP API:
8276989335:AAEMMygR7yaUlCV7WhMoI0WP6u5wf2MiOls")
print(f"1. Check for BOT_TOKEN: {'Found' if bot_token else 'NOT FOUND'}")

if bot_token and bot_token.startswith("8276989335"):
    print("2. The token starts correctly with '8276989335'.")
elif not bot_token:
    print("2. ERROR: Environment variable 'BOT_TOKEN' is empty or not set.")
    print("   Please check your Environment Variables in the Render Dashboard.")
    sys.exit(1)
else:
    print(f"2. WARNING: The token value seems different. Value: {bot_token[:10]}...")
    sys.exit(1)

print("3. All checks passed. The environment is ready.")
print("--- Test Complete ---")
