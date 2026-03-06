import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Cloud Build App</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #0a0a0f;
      --surface: #111118;
      --border: rgba(255,255,255,0.07);
      --accent: #00f5a0;
      --accent2: #00d9f5;
      --text: #e8e8f0;
      --muted: #6b6b80;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Syne', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(0,245,160,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,217,245,0.07) 0%, transparent 60%);
      pointer-events: none;
      z-index: 0;
    }
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
      z-index: 0;
    }
    .container {
      position: relative;
      z-index: 1;
      max-width: 900px;
      margin: 0 auto;
      padding: 60px 24px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(0,245,160,0.1);
      border: 1px solid rgba(0,245,160,0.25);
      border-radius: 100px;
      padding: 6px 16px;
      font-family: 'DM Mono', monospace;
      font-size: 12px;
      color: var(--accent);
      margin-bottom: 40px;
      animation: fadeUp 0.6s ease both;
    }
    .dot {
      width: 7px; height: 7px;
      background: var(--accent);
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.8); }
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(20px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    h1 {
      font-size: clamp(42px, 8vw, 80px);
      font-weight: 800;
      line-height: 1;
      letter-spacing: -2px;
      margin-bottom: 20px;
      animation: fadeUp 0.6s 0.1s ease both;
    }
    h1 span {
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .subtitle {
      font-size: 18px;
      color: var(--muted);
      max-width: 500px;
      line-height: 1.6;
      margin-bottom: 60px;
      animation: fadeUp 0.6s 0.2s ease both;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 60px;
      animation: fadeUp 0.6s 0.3s ease both;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      transition: border-color 0.3s, transform 0.3s;
    }
    .card:hover {
      border-color: rgba(0,245,160,0.3);
      transform: translateY(-4px);
    }
    .card-icon { font-size: 28px; margin-bottom: 16px; }
    .card-title {
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--muted);
      margin-bottom: 8px;
    }
    .card-value {
      font-family: 'DM Mono', monospace;
      font-size: 15px;
      color: var(--accent);
      word-break: break-all;
    }
    .status-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 32px;
      animation: fadeUp 0.6s 0.4s ease both;
    }
    .status-left { display: flex; align-items: center; gap: 12px; }
    .status-indicator {
      width: 10px; height: 10px;
      background: var(--accent);
      border-radius: 50%;
      box-shadow: 0 0 12px var(--accent);
      animation: pulse 2s infinite;
    }
    .status-text { font-size: 15px; color: var(--text); }
    .status-text span { color: var(--accent); font-weight: 700; }
    .api-btn {
      font-family: 'DM Mono', monospace;
      font-size: 13px;
      background: rgba(0,245,160,0.1);
      color: var(--accent);
      border: 1px solid rgba(0,245,160,0.3);
      border-radius: 8px;
      padding: 8px 18px;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.2s;
    }
    .api-btn:hover { background: rgba(0,245,160,0.2); }
    .pipeline {
      display: flex;
      align-items: center;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      overflow-x: auto;
      animation: fadeUp 0.6s 0.5s ease both;
      margin-bottom: 60px;
    }
    .step {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      min-width: 90px;
    }
    .step-icon {
      width: 44px; height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      background: rgba(0,245,160,0.1);
      border: 1px solid rgba(0,245,160,0.2);
    }
    .step-label {
      font-size: 11px;
      font-family: 'DM Mono', monospace;
      color: var(--muted);
      text-align: center;
    }
    .step-arrow {
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, var(--accent), var(--accent2));
      min-width: 20px;
      opacity: 0.4;
    }
    footer {
      text-align: center;
      font-family: 'DM Mono', monospace;
      font-size: 12px;
      color: var(--muted);
      animation: fadeUp 0.6s 0.6s ease both;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">
      <div class="dot"></div>
      LIVE ON GOOGLE CLOUD RUN
    </div>

    <h1>Hello from<br/><span>Cloud Build!</span></h1>
    <p class="subtitle">Deployed automatically via Cloud Build pipeline. Built with Docker, stored in Artifact Registry, served on Cloud Run.</p>

    <div class="grid">
      <div class="card">
        <div class="card-icon">🚀</div>
        <div class="card-title">Status</div>
        <div class="card-value">running</div>
      </div>
      <div class="card">
        <div class="card-icon">🌍</div>
        <div class="card-title">Region</div>
        <div class="card-value">asia-south1</div>
      </div>
      <div class="card">
        <div class="card-icon">📦</div>
        <div class="card-title">Platform</div>
        <div class="card-value">Cloud Run</div>
      </div>
      <div class="card">
        <div class="card-icon">🔧</div>
        <div class="card-title">Built With</div>
        <div class="card-value">Python + Flask</div>
      </div>
    </div>

    <div class="status-bar">
      <div class="status-left">
        <div class="status-indicator"></div>
        <div class="status-text">Service is <span>healthy</span> and accepting traffic</div>
      </div>
      <a class="api-btn" href="/health">health check →</a>
    </div>

    <div class="pipeline">
      <div class="step">
        <div class="step-icon">💻</div>
        <div class="step-label">Code Push</div>
      </div>
      <div class="step-arrow"></div>
      <div class="step">
        <div class="step-icon">⚙️</div>
        <div class="step-label">Cloud Build</div>
      </div>
      <div class="step-arrow"></div>
      <div class="step">
        <div class="step-icon">🐳</div>
        <div class="step-label">Docker Image</div>
      </div>
      <div class="step-arrow"></div>
      <div class="step">
        <div class="step-icon">📦</div>
        <div class="step-label">Artifact Registry</div>
      </div>
      <div class="step-arrow"></div>
      <div class="step">
        <div class="step-icon">☁️</div>
        <div class="step-label">Cloud Run</div>
      </div>
    </div>

    <footer>vamsi-project-488603 &nbsp;·&nbsp; demo-repo &nbsp;·&nbsp; asia-south1</footer>
  </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api')
def api():
    return jsonify({
        "message": "Hello from Cloud Build!",
        "status": "running"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
