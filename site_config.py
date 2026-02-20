from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass(frozen=True)
class Link:
    label: str
    url: str
    target: Optional[str] = None


@dataclass(frozen=True)
class Page:
    path: str              # "/", "/bio/", etc
    template: str          # "index.html", "bio.html"
    output_dir: str        # "" for root, "bio" for /bio/


@dataclass(frozen=True)
class SiteConfig:
    band_name: str
    tagline: str
    links: List[Link]
    year: int

    def template_context(self) -> Dict[str, object]:
        return {
            "band_name": self.band_name,
            "tagline": self.tagline,
            "links": [link.__dict__ for link in self.links],
            "year": self.year,
        }


def load_site_config() -> SiteConfig:
    return SiteConfig(
        band_name="In the Company of Serpents",
        tagline="Sonic Catharsis",
        links=[
            Link(label="Bandcamp", url="https://inthecompanyofserpentsdoom.bandcamp.com/", target="_blank"),
            Link(label="Instagram", url="https://www.instagram.com/itcosdoom/", target="_blank"),
            Link(label="Bio", url="bio/"),
            Link(label="Email", url="mailto:inthecompanyofserpents@gmail.com", target="_blank"),
        ],
        year=datetime.now().year,
    )


def load_pages() -> List[Page]:
    return [
        Page(path="/", template="index.html", output_dir=""),
        Page(path="/bio/", template="bio.html", output_dir="bio"),
    ]