import argparse

from site_builder import BuildPaths, build_site, create_app as create_flask_app
from site_config import load_pages, load_site_config


def create_app(paths: BuildPaths | None = None):
    config = load_site_config()
    app = create_flask_app(paths or BuildPaths())

    for page in load_pages():
        endpoint = page.path.strip("/").replace("/", "_") or "index"

        def render_page(page=page):
            return app.jinja_env.get_template(page.template).render(**config.template_context(page=page))

        app.add_url_rule(page.path, endpoint, render_page)
        if page.path != "/":
            app.add_url_rule(page.path.rstrip("/"), f"{endpoint}_no_slash", render_page)

    return app


def serve(port: int, debug: bool) -> None:
    app = create_app()

    app.run(host="127.0.0.1", port=port, debug=debug)


def main() -> None:
    parser = argparse.ArgumentParser(description="itcos site builder")
    sub = parser.add_subparsers(dest="command", required=True)

    p_serve = sub.add_parser("serve", help="Run local dev server")
    p_serve.add_argument("--port", type=int, default=5000)
    p_serve.add_argument("--debug", action="store_true")

    p_build = sub.add_parser("build", help="Build static site into dist/")
    p_build.add_argument("--out", default="dist", help="Output directory (default: dist)")
    p_build.add_argument("--no-clean", action="store_true", help="Do not delete dist/ before building")
    p_build.add_argument(
        "--site-url",
        default="https://inthecompanyofserpents.com",
        help="Site URL for sitemap generation",
    )

    args = parser.parse_args()

    config = load_site_config()

    if args.command == "serve":
        serve(port=args.port, debug=args.debug)
        return

    if args.command == "build":
        paths = BuildPaths(dist_dir=args.out)
        pages = load_pages()
        build_site(config, pages, paths, clean=(not args.no_clean), site_url=args.site_url)


if __name__ == "__main__":
    main()