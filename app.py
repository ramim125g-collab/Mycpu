from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MyBinder Code Runner</title>
    <style>
        body { font-family: Arial; background: #121212; color: #fff; padding: 20px; }
        textarea { width: 100%; height: 150px; background: #1e1e1e; color: #0f0; padding: 10px; font-family: monospace; font-size: 16px; border: 1px solid #444; }
        input[type="submit"] { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; font-size: 16px; }
        pre { background: #1e1e1e; padding: 15px; border: 1px solid #444; white-space: pre-wrap; color: #ff0; }
    </style>
</head>
<body>
    <h2>Cloud Code Runner (MyBinder)</h2>
    <form method="POST">
        <textarea name="cmd" placeholder="Enter linux command or python script here...">{{ cmd }}</textarea><br>
        <input type="submit" value="Run">
    </form>
    <h3>Output:</h3>
    <pre>{{ output }}</pre>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ""
    cmd = ""
    if request.method == 'POST':
        cmd = request.form.get('cmd')
        try:
            # Execute command in linux shell
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            output = res.stdout + res.stderr
        except Exception as e:
            output = str(e)
    return render_template_string(HTML_PAGE, output=output, cmd=cmd)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
