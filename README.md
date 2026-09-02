# ITCOS

## Run Locally

Create and activate the virtual environment, install dependencies, and start Flask:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python app.py serve

Open http://127.0.0.1:5000/ in your browser. After `.venv` has been created, future sessions only require:

    source .venv/bin/activate
    python app.py serve

While actively editing templates or CSS, use debug mode:

    python app.py serve --debug

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
