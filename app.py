import argparse

from site_builder import BuildPaths, build_site, create_app
from site_config import load_site_config, load_pages


def serve(port: int, debug: bool) -> None:
    config = load_site_config()
    paths = BuildPaths()
    app = create_app(paths)

    @app.route("/")
    def index():
        return app.jinja_env.get_template(paths.index_template).render(**config.template_context())
    
    @app.route("/bio")
    @app.route("/bio/")
    def bio():
        return app.jinja_env.get_template("bio.html").render(**config.template_context())

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