
import argparse
import os
import shutil
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

TEMPLATE = "index.html"
STATIC_SRC = os.path.join("static", "styles.css")
STATIC_DST = os.path.join("dist", "styles.css")
DIST_DIR = "dist"

DATA = {
  "band_name": "In the Company of Serpents",
  "tagline": "Sonic Catharsis",
  "links": [
    {"label": "Bandcamp", "url": "https://inthecompanyofserpentsdoom.bandcamp.com/"},
    {"label": "Instagram", "url": "https://www.instagram.com/itcosdoom/"},
    {"label": "Email", "url": "mailto:inthecompanyofserpents@gmail.com"},
  ],
  "year": datetime.now().year,
}

def build():
    os.makedirs(DIST_DIR, exist_ok=True)

    # Render HTML (template can use url_for('static', ...))
    with app.test_request_context("/"):
        html = render_template(TEMPLATE, **DATA)

    # Write index.html
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Copy static/ -> dist/static/
    dist_static = os.path.join(DIST_DIR, "static")
    if os.path.exists(dist_static):
        shutil.rmtree(dist_static)
    shutil.copytree("static", dist_static)

    print("ITCOS Build complete: dist/index.html and dist/static/* copied.")



def serve():
  app = Flask(__name__, template_folder="templates", static_folder="static")

  @app.route("/")
  def index():
    return render_template(TEMPLATE, **DATA)

  app.run(debug=True)

def main():
  parser = argparse.ArgumentParser(description="itcos site builder")
  parser.add_argument("command", choices=["serve", "build"], help="Command to run")
  args = parser.parse_args()
  if args.command == "build":
    build()
  elif args.command == "serve":
    serve()

if __name__ == "__main__":
  main()
