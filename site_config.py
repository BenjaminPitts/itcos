from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Link:
    label: str
    url: str
    target: Optional[str] = None


@dataclass(frozen=True)
class Page:
    path: str              # "/"
    template: str          # "index.html"
    output_dir: str        # "" for root


@dataclass(frozen=True)
class Quote:
    source: str
    text: str
    url: Optional[str] = None
    homepage_column: Optional[str] = None


@dataclass(frozen=True)
class SiteConfig:
    band_name: str
    tagline: str
    descriptor: str
    site_url: str
    contact_email: str
    social_links: List[Link]
    navigation: List[Link]
    featured_album: Dict[str, str]
    videos: List[Dict[str, str]]
    press_quotes: List[Quote]
    latest_press_release: Dict[str, str]
    highlights: List[str]
    shows: List[Dict[str, str]]
    epk_url: Optional[str]
    year: int

    def template_context(self, *, page: Optional[Page] = None) -> Dict[str, object]:
        page_path = page.path if page else "/"
        page_meta = {
            "/": {
                "title": "In the Company of Serpents | Denver Sludge & Doom Metal",
                "description": "Official site of Denver sludge and doom band In the Company of Serpents. Listen to A Crack in Everything, watch videos, view tour dates, press, and booking information.",
            },
        }
        return {
            "band_name": self.band_name,
            "tagline": self.tagline,
            "descriptor": self.descriptor,
            "site_url": self.site_url,
            "contact_email": self.contact_email,
            "social_links": [link.__dict__ for link in self.social_links],
            "navigation": [link.__dict__ for link in self.navigation],
            "featured_album": self.featured_album,
            "videos": self.videos,
            "press_quotes": [quote.__dict__ for quote in self.press_quotes],
            "latest_press_release": self.latest_press_release,
            "highlights": self.highlights,
            "shows": self.shows,
            "epk_url": self.epk_url,
            "canonical_url": f"{self.site_url.rstrip('/')}{page_path}",
            "page_title": page_meta.get(page_path, page_meta["/"])["title"],
            "page_description": page_meta.get(page_path, page_meta["/"])["description"],
            "year": self.year,
        }


def load_site_config() -> SiteConfig:
    return SiteConfig(
        band_name="In the Company of Serpents",
        tagline="Sonic Catharsis",
        descriptor="Denver sludge / doom inhabiting the strange fringes between crushing metal and sprawling spaghetti western scores.",
        site_url="https://inthecompanyofserpents.com",
        contact_email="inthecompanyofserpents@gmail.com",
        navigation=[
            Link(label="About", url="/#about"), Link(label="Listen", url="/#listen"),
            Link(label="Watch", url="/#watch"), Link(label="Shows", url="/#shows"),
            Link(label="Press", url="/#press"), Link(label="Contact", url="/#contact"),
        ],
        social_links=[
            Link(label="Instagram", url="https://www.instagram.com/itcosdoom/", target="_blank"),
            Link(label="Facebook", url="https://www.facebook.com/InTheCompanyOfSerpents", target="_blank"),
            Link(label="Bandcamp", url="https://inthecompanyofserpentsdoom.bandcamp.com/", target="_blank"),
        ],
        featured_album={"title": "A Crack in Everything", "year": "2025", "url": "https://inthecompanyofserpentsdoom.bandcamp.com/", "embed_url": "https://bandcamp.com/EmbeddedPlayer/album=891941117/size=large/bgcol=333333/linkcol=0f91ff/artwork=small/transparent=true/"},
        videos=[
            {"title": "A Patchwork Art", "url": "https://www.youtube.com/embed/28WZRge2fUk"},
            {"title": "Record Release Show for A Crack in Everything", "url": "https://www.youtube.com/embed/DUcCrHVpAzA"},
        ],
        press_quotes=[
            Quote("Everything Is Noise", "IN THE COMPANY OF SERPENTS so expertly combine the heft of doom and the general ambience of Colorado and the Mountain region it’s in. It takes a palmful of dirt and smacks it on the haunches of their metal music to grit it up.", "https://everythingisnoise.net/premieres/wily-denver-doomers-in-the-company-of-serpents-show-us-a-crack-in-everything/", "long"),
            Quote("Decibel Magazine", "…if it seems that Denver sludge trio IN THE COMPANY OF SERPENTS are pursuing an unusual sonic path on their latest single, ‘A Patchwork Art,’ be patient, because what sounds like a Spaghetti Western theme soon erupts into a massive slab of ear crush. The light and dark sides of the song continue to do battle, until the doom ultimately snuffs out any whiff of the Old West. This is just full-on dire sludge, no apologies.", "https://www.decibelmagazine.com/2025/06/23/video-premiere-in-the-company-of-serpents-a-patchwork-of-art/", "long"),
            Quote("New Noise Magazine", "…a powerful sojourn into the depths of darkness, through riffs of mile high doom and gloom, a document not of a victim but as a survivor.", "https://newnoisemagazine.com/interviews/interview-in-the-company-of-serpents-talk-new-record/", "short"),
            Quote("No Clean Singing", "…while there’s an undeniable sense of weight and thick, almost oppressive, presence to songs such ‘Endless Well’ and ‘Ghosts On The Periphery’ there’s also an undercurrent of something more subtle – an unexpected lightness of being, perhaps – which feels like the sloughing off of old scars and the beginnings, at least, of some long-sought catharsis manifesting in moments like the melancholy clean vocals of the former and the somber atmospherics of the latter.", "https://www.nocleansinging.com/2025/09/12/gonzos-heavy-roundup-end-of-summer-edition-2025/"),
            Quote("Wonderbox Metal", "…an album that spends its duration well, covering its gritty bases, while soaring to the heavens. It contains some of the band’s most satisfying material and is likely to be considered as their strongest album so far."),
            Quote("Heavy Music HQ", "It’s not often that a band almost 15 years into their career has hit their stride, but IN THE COMPANY OF SERPENTS prove to do so with A Crack In Everything.", "https://heavymusichq.com/heavy-music-hq-reviews-week-of-july-11-2025/", "short"),
            Quote("Ghost Cult", "The riffs are simple but huge, the production makes the whole thing heavier than a sack of spanners, and the overall effect is undeniably compelling. If you want to experience being pulped by a herd of slowly stampeding elephants, then just listen to A Crack In Everything.", "https://ghostcultmag.com/album-review-in-the-company-of-serpents-a-crack-in-everything-self-released/"),
        ],
        latest_press_release={
            "title": "U.S. tour dates announced",
            "snippet": "In the Company of Serpents announce U.S. tour dates surrounding Asheville Doomed & Stoned Fest this July (2026).",
            "url": "https://www.earsplitcompound.com/in-the-company-of-serpents-announces-us-tour-dates-surrounding-asheville-doomed-and-stoned-fest-this-july/",
        },
        highlights=["Decibel Magazine Top 40 Albums of the Year — 2020 and 2025", "Shared stages with Neurosis, Sleep, Red Fang, YOB, Converge, Godflesh, and more"],
        shows=[],
        epk_url="https://drive.google.com/file/d/1LgvzdvKIkp65EQtodECvXwcCnWSfd4_5/view?usp=sharing",
        year=datetime.now().year,
    )


def load_pages() -> List[Page]:
    return [Page(path="/", template="index.html", output_dir="")]