# ITCOS

## Run Locally (Flask Dev Server)

Create and activate a virtual environment, then install dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Start the development server:

    python app.py serve

Open in your browser:
http://127.0.0.1:5000

---

## Build Static Site

Generate the static build:

    python app.py build

This creates the `dist/` directory.

To preview the static build:

    cd dist
    python3 -m http.server 8080

Open in your browser:
http://localhost:8080
