import os
import subprocess


def install_npm_packages():
  print("[SETUP] Installing Node.js dependencies (bedrock-protocol)...")
  subprocess.run(["npm", "install", "bedrock-protocol"], check=True)


def start_bot():
  try:
    install_npm_packages()
  except Exception as e:
    print(f"[ERROR] NPM install failed: {e}")

  host = os.environ.get("MC_HOST", "localhost")
  port = os.environ.get("MC_PORT", "25565")
  bot_name = os.environ.get("BOT_NAME", "CraftBot_Pro")

  print(f"[RUNNER] Starting Bot -> Target: {host}:{port} | Name: {bot_name}")

  env = os.environ.copy()
  env["MC_HOST"] = host
  env["MC_PORT"] = port
  env["BOT_NAME"] = bot_name

  process = subprocess.Popen(
      ["node", "bedrock_bot.js"],
      env=env,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
  )

  # Render ba local console-e live log dekhar jonno
  while True:
    output = process.stdout.readline()
    if output == "" and process.poll() is not None:
      break
    if output:
      print(output.strip(), flush=True)


if __name__ == "__main__":
  start_bot()
