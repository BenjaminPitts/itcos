# ITCOS

## Run Locally (Flask Dev Server)

Activate a virtual environment:

    source .venv/bin/activate

Start the development server:

    python app.py serve

Open in your browser:
http://127.0.0.1:5000

---

## Build Static Site

ITCOS is hosted on Netlify, which builds the project on git push,
but here's the steps to generate a static build:

    python app.py build

This creates the `dist/` directory.

To preview the static build:

    cd dist
    python3 -m http.server 8080

Open in your browser:
http://localhost:8080
