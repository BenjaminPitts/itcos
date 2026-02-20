from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from flask import Flask, render_template

from site_config import SiteConfig, Page


@dataclass(frozen=True)
class BuildPaths:
    dist_dir: str = "dist"
    templates_dir: str = "templates"
    static_dir: str = "static"
    robots_src: str = "robots.txt"

    @property
    def dist_static_dir(self) -> str:
        return os.path.join(self.dist_dir, "static")


def create_app(paths: BuildPaths) -> Flask:
    return Flask(
        __name__,
        template_folder=paths.templates_dir,
        static_folder=paths.static_dir,
    )


def clean_dist(dist_dir: str) -> None:
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def copy_if_exists(src: str, dst: str) -> None:
    if os.path.exists(src):
        shutil.copy2(src, dst)


def copy_tree(src_dir: str, dst_dir: str) -> None:
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)


def generate_sitemap_xml(site_url: str, pages: list[Page], lastmod: Optional[str] = None) -> str:
    if not lastmod:
        lastmod = datetime.now(timezone.utc).date().isoformat()

    base = site_url.rstrip("/")
    urls = []
    for p in pages:
        loc = f"{base}{p.path}"
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <priority>1.0</priority>
  </url>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""


def build_site(config: SiteConfig, pages: list[Page], paths: BuildPaths, *, clean: bool = True, site_url: str = "") -> None:
    if clean:
        clean_dist(paths.dist_dir)

    ensure_dir(paths.dist_dir)

    app = create_app(paths)
    ctx = config.template_context()

    # Render + write each page
    with app.test_request_context("/"):
        for page in pages:
            html = render_template(page.template, **ctx)
            out_dir = paths.dist_dir if page.output_dir == "" else os.path.join(paths.dist_dir, page.output_dir)
            ensure_dir(out_dir)
            write_file(os.path.join(out_dir, "index.html"), html)

        # Root 404.html for Netlify
        not_found_html = render_template("404.html", **ctx)
        write_file(os.path.join(paths.dist_dir, "404.html"), not_found_html)

    # robots.txt
    copy_if_exists(paths.robots_src, os.path.join(paths.dist_dir, "robots.txt"))

    # sitemap.xml
    if site_url:
        sitemap = generate_sitemap_xml(site_url.rstrip("/") + "/", pages)
        write_file(os.path.join(paths.dist_dir, "sitemap.xml"), sitemap)

    # static assets
    copy_tree(paths.static_dir, paths.dist_static_dir)

    print(f"✅ ITCOS Build complete: {paths.dist_dir}/")