import os
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


# 1. Choto ekta dummy HTTP server (Render-er port requirement puron korar jonno)
class SimpleHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Minecraft Bot is running successfully!")


def run_web_server():
  port = int(os.environ.get("PORT", 10000))  # Render automatic PORT assign kore
  server = HTTPServer(("0.0.0.0", port), SimpleHandler)
  print(f"[WEB SERVER] Running on port {port}...")
  server.serve_forever()


# 2. Node.js Bedrock Bot run korar function
def start_bot():
  print("[SETUP] Installing Node.js dependencies (bedrock-protocol)...")
  try:
    subprocess.run(["npm", "install", "bedrock-protocol"], check=True)
  except Exception as e:
    print(f"[ERROR] NPM install failed: {e}")

  host = os.environ.get("MC_HOST", "Killanimal.aternos.me")
  port = os.environ.get("MC_PORT", "25565")
  bot_name = os.environ.get("BOT_NAME", "CramimraftBot_Pro")

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

  while True:
    output = process.stdout.readline()
    if output == "" and process.poll() is not None:
      break
    if output:
      print(output.strip(), flush=True)


if __name__ == "__main__":
  # Web server-tike alada thread-e chalu rakha jate main thread bot-ke chalate pare
  web_thread = threading.Thread(target=run_web_server, daemon=True)
  web_thread.start()

  # Bot start kora
  start_bot()
