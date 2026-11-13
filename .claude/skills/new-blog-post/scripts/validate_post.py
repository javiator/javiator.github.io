#!/usr/bin/env python3
"""Validate blog posts against the site's conventions.

Usage:
  validate_post.py <post.md> [...]   strict check of new/edited posts (exit 1 on errors)
  validate_post.py --all [-v]        check every post; legacy convention warnings hidden unless -v
  validate_post.py --taxonomy        print categories, tags, series and evolutions in use
  validate_post.py --url <post.md>   print the URL path the post will be published at
"""
import datetime
import glob
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TAX = yaml.safe_load(open(os.path.join(HERE, "..", "taxonomy.yml"), encoding="utf-8"))

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = ["title", "date", "permalink", "categories", "tags", "excerpt",
            "content_type", "learning_focus", "difficulty", "header"]


def kebab(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def data(name):
    path = os.path.join(ROOT, "_data", name)
    return yaml.safe_load(open(path, encoding="utf-8")) if os.path.exists(path) else {}


def load(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        raise ValueError("file does not start with front matter '---'")
    _, fm, body = text.split("---\n", 2)
    return yaml.safe_load(fm) or {}, body


def all_posts():
    return sorted(glob.glob(os.path.join(ROOT, "_posts", "**", "*.md"), recursive=True))


def slug_of(path):
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path))[:-3]


def url_of(path, fm):
    if fm.get("permalink"):
        return fm["permalink"]
    cats = "/".join(str(c).lower() for c in fm.get("categories") or [])
    return "/%s/%s/" % (cats, slug_of(path)) if cats else "/%s/" % slug_of(path)


def expected_permalink(path, fm):
    return "/" + "/".join([kebab(c) for c in fm.get("categories") or []] + [slug_of(path)]) + "/"


def asset_exists(ref):
    return os.path.isfile(os.path.join(ROOT, ref.lstrip("/")))


class Report:
    def __init__(self, path, strict):
        self.path, self.strict, self.items = path, strict, []

    def err(self, msg):          # always an error: the site would be broken
        self.items.append(("ERROR", msg))

    def conv(self, msg):         # convention: error for new posts, warning for legacy ones
        self.items.append(("ERROR" if self.strict else "WARN", msg))

    def warn(self, msg):
        self.items.append(("WARN", msg))

    def note(self, msg):
        self.items.append(("NOTE", msg))

    @property
    def errors(self):
        return [m for level, m in self.items if level == "ERROR"]


def check(path, strict, others):
    r = Report(os.path.relpath(path, ROOT), strict)
    try:
        fm, body = load(path)
    except Exception as exc:  # noqa: BLE001
        r.err("cannot parse front matter: %s" % exc)
        return r

    name = os.path.basename(path)
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9-]+)\.md$", name)
    if not m:
        r.err("filename must be YYYY-MM-DD-kebab-slug.md")
        return r
    year, month, day, slug = m.groups()
    rel = os.path.relpath(path, os.path.join(ROOT, "_posts"))
    if os.path.dirname(rel) != "%s/%s" % (year, month):
        r.conv("post should live in _posts/%s/%s/" % (year, month))

    # --- front matter ---------------------------------------------------
    for key in REQUIRED:
        if fm.get(key) in (None, "", []):
            r.conv("missing front matter: %s" % key)
    for key in TAX["forbidden_keys"]:
        if key in fm:
            r.conv("remove front matter key '%s'%s" % (
                key, " (use 'featured')" if key == "feature" else
                " (use 'excerpt')" if key == "description" else ""))

    title = str(fm.get("title") or "")
    if "\n" in title:
        r.conv("title must be a single line")
    date = fm.get("date")
    if isinstance(date, (datetime.date, datetime.datetime)):
        if date.strftime("%Y-%m-%d") != "%s-%s-%s" % (year, month, day):
            r.err("front matter date %s does not match filename date" % date)
        if strict and date.strftime("%Y-%m-%d") > datetime.date.today().isoformat():
            r.warn("date is in the future: GitHub Pages will not publish it until then")
    elif date is not None:
        r.err("date must be YYYY-MM-DD")

    cats = fm.get("categories") or []
    primary, topics = TAX["categories"]["primary"], TAX["categories"]["topics"]
    if not isinstance(cats, list):
        r.err("categories must be a list")
        cats = []
    if cats:
        if not 2 <= len(cats) <= 3:
            r.conv("use 2-3 categories (1 primary + 1-2 topics), found %d" % len(cats))
        if cats[0] not in primary:
            r.conv("first category must be one of %s, found '%s'" % (list(primary), cats[0]))
        for c in cats[1:]:
            if c not in topics:
                r.conv("category '%s' is not in taxonomy.yml topics %s" % (c, list(topics)))
        if any("/" in str(c) for c in cats):
            r.conv("categories must not contain '/' (it creates nested URLs)")
        if len(set(cats)) != len(cats):
            r.conv("duplicate categories")

    if fm.get("permalink"):
        if not re.match(r"^/[a-z0-9/-]+/$", fm["permalink"]):
            r.err("permalink must be lowercase kebab segments with leading and trailing '/'")
        elif strict and cats and fm["permalink"] != expected_permalink(path, fm):
            r.conv("permalink should be %s" % expected_permalink(path, fm))

    tags = fm.get("tags") or []
    if not isinstance(tags, list):
        r.err("tags must be a list")
        tags = []
    for t in tags:
        if not KEBAB.match(str(t)):
            r.conv("tag '%s' must be kebab-case" % t)
    if tags and not TAX["tags"]["min"] <= len(tags) <= TAX["tags"]["max"]:
        r.conv("use %d-%d tags, found %d" % (TAX["tags"]["min"], TAX["tags"]["max"], len(tags)))
    used = {t for p, (f, _) in others.items() if p != path for t in (f.get("tags") or [])}
    new = [t for t in tags if t not in used]
    if strict and new:
        r.note("tags not used by any other post (confirm they are intended): %s" % ", ".join(new))

    if fm.get("content_type") and fm["content_type"] not in TAX["content_types"]:
        r.conv("content_type '%s' not in taxonomy.yml" % fm["content_type"])
    if fm.get("difficulty") and fm["difficulty"] not in TAX["difficulty"]:
        r.conv("difficulty must be one of %s" % TAX["difficulty"])
    lf = fm.get("learning_focus")
    if lf and (not isinstance(lf, list) or any(not KEBAB.match(str(x)) for x in lf)):
        r.conv("learning_focus must be a list of kebab-case topics")
    if fm.get("excerpt") and len(str(fm["excerpt"])) > 320:
        r.warn("excerpt is long (%d chars); aim for 1-2 sentences" % len(str(fm["excerpt"])))

    # --- images -----------------------------------------------------------
    header = fm.get("header") or {}
    for key in ("overlay_image", "teaser"):
        ref = header.get(key)
        if not ref:
            r.conv("missing header.%s" % key)
        elif not asset_exists(ref):
            r.err("header.%s file not found: %s" % (key, ref))
    if header.get("overlay_image") and header.get("overlay_filter") is None:
        r.conv("set header.overlay_filter: 0.5 so the title is readable over the image")
    asset_dir = "/assets/images/posts/%s/%s/%s/" % (year, month, slug)
    refs = set(re.findall(r"""(?:\]\(|src=["'])(/assets/[^)\s"']+)""", body))
    for ref in sorted(refs):
        if not asset_exists(ref):
            r.err("referenced file not found: %s" % ref)
        elif strict and not ref.startswith(asset_dir):
            r.warn("new images belong in %s (found %s)" % (asset_dir, ref))
    if strict and header.get("overlay_image") and not header["overlay_image"].startswith(asset_dir):
        r.warn("header image is outside %s (fine only if deliberately reusing an image)" % asset_dir)
    for alt in re.findall(r"!\[(.*?)\]\(", body):
        if not alt.strip():
            r.conv("image without alt text")
            break

    # --- body ---------------------------------------------------------------
    no_code = re.sub(r"(?s)```.*?```", "", body)
    if re.search(r"(?m)^# \S", no_code):
        r.conv("body must not contain an H1 ('# '); the theme renders the title")
    has_mermaid = "```mermaid" in body
    if has_mermaid and not fm.get("mermaid"):
        r.err("body has mermaid blocks but front matter lacks 'mermaid: true'")
    if fm.get("mermaid") and not has_mermaid:
        r.conv("'mermaid: true' set but the body has no mermaid blocks")
    if (re.search(r"(?i)\blorem ipsum\b", no_code) or re.search(r"\b(TODO|TBD|PLACEHOLDER)\b|<[A-Z][^>\n]*>", no_code)) and strict:
        r.warn("possible placeholder text left in the body")
    if strict and len(no_code.split()) < 300:
        r.warn("post is short (%d words)" % len(no_code.split()))

    # --- series -------------------------------------------------------------
    series = fm.get("series")
    if series:
        if series not in data("series.yml"):
            r.err("series '%s' is not defined in _data/series.yml" % series)
        if not os.path.isfile(os.path.join(ROOT, "_pages", "series", series, "index.md")):
            r.err("missing series page _pages/series/%s/index.md" % series)
        order = fm.get("series_order")
        if not isinstance(order, int):
            r.conv("series posts need an integer series_order")
        else:
            clash = [os.path.basename(p) for p, (f, _) in others.items()
                     if p != path and f.get("series") == series and f.get("series_order") == order]
            if clash:
                r.err("series_order %d already used by %s" % (order, ", ".join(clash)))
    elif "series_order" in fm:
        r.conv("series_order set without series")

    # --- evolution / project -----------------------------------------------
    if fm.get("project"):
        pid = kebab(fm["project"])
        evolutions = data("evolutions.yml").get(pid)
        if pid not in data("projects.yml") or evolutions is None:
            r.err("project '%s' is not defined in _data/projects.yml and _data/evolutions.yml" % fm["project"])
        else:
            num = fm.get("evolution_number")
            evo = next((e for e in evolutions if e.get("number") == num), None)
            if num is None:
                r.err("project posts need evolution_number")
            elif evo is None and num != 0:
                r.err("evolution_number %s is not defined in _data/evolutions.yml" % num)
            elif evo:
                want = "Evolution %s: %s" % (num, evo["title"])
                if fm.get("evolution") != want:
                    r.conv("evolution should be \"%s\"" % want)
                if not os.path.isfile(os.path.join(ROOT, "_pages", evo["url"].strip("/"), "index.md")):
                    r.err("missing evolution page for %s" % evo["url"])
            for key in ("project_type", "evolution_focus"):
                if not fm.get(key):
                    r.conv("project posts need %s" % key)
            for inc in ("evolution/evolution-posts.html", "evolution/post-navigation.html"):
                if num != 0 and ("{% include " + inc) not in body:
                    r.conv("project posts must end with {%% include %s %%}" % inc)
    elif any(k in fm for k in ("evolution", "evolution_number", "evolution_focus")):
        r.err("evolution fields set without project")

    # --- uniqueness ----------------------------------------------------------
    url = url_of(path, fm)
    for p, (f, _) in others.items():
        if p != path and url_of(p, f) == url:
            r.err("URL %s is already used by %s" % (url, os.path.basename(p)))
        if p != path and slug_of(p) == slug:
            r.err("slug '%s' is already used by %s" % (slug, os.path.basename(p)))
    return r


def taxonomy():
    from collections import Counter
    cats, tags = Counter(), Counter()
    series_count, evo_count = Counter(), Counter()
    for p in all_posts():
        fm, _ = load(p)
        cats.update(fm.get("categories") or [])
        tags.update(fm.get("tags") or [])
        if fm.get("series"):
            series_count[fm["series"]] += 1
        if fm.get("project"):
            evo_count[(kebab(fm["project"]), fm.get("evolution_number"))] += 1
    print("# Categories allowed for new posts")
    for group in ("primary", "topics"):
        for name, desc in TAX["categories"][group].items():
            print("  [%s] %-17s %s" % (group, name, desc))
    print("\n# Content types\n  " + ", ".join(TAX["content_types"]))
    print("\n# Tags in use (count)")
    print("  " + ", ".join("%s(%d)" % kv for kv in sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))))
    print("\n# Series (_data/series.yml)")
    for sid, s in data("series.yml").items():
        print("  %-18s %-26s posts=%d next series_order=%d status=%s" % (
            sid, s.get("title"), series_count[sid], series_count[sid] + 1, s.get("status")))
    print("\n# Projects and evolutions (_data/evolutions.yml)")
    for pid, evos in data("evolutions.yml").items():
        print("  project id=%s  front matter value=\"%s\"" % (
            pid, " ".join(w.capitalize() for w in pid.split("-"))))
        for e in evos:
            print("    Evolution %s: %-30s status=%-9s posts=%d" % (
                e["number"], e["title"], e.get("status"), evo_count[(pid, e["number"])]))
    print("\n# Legacy categories on older posts (do not use for new posts)")
    allowed = set(TAX["categories"]["primary"]) | set(TAX["categories"]["topics"])
    print("  " + ", ".join(sorted(c for c in cats if c not in allowed)))


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--taxonomy":
        taxonomy()
        return 0
    if argv[0] == "--url":
        fm, _ = load(argv[1])
        print(url_of(os.path.abspath(argv[1]), fm))
        return 0
    strict = argv[0] != "--all"
    verbose = strict or "-v" in argv
    hidden = 0
    targets = [os.path.abspath(a) for a in argv] if strict else all_posts()
    others = {}
    for p in all_posts():
        try:
            others[p] = load(p)
        except Exception:  # noqa: BLE001
            others[p] = ({}, "")
    failed = False
    for t in targets:
        if not os.path.isfile(t):
            print("ERROR  %s: file not found" % t)
            failed = True
            continue
        r = check(t, strict, others)
        shown = [i for i in r.items if verbose or i[0] == "ERROR"]
        hidden += len(r.items) - len(shown)
        if shown:
            print(r.path)
            for level, msg in shown:
                print("  %-5s %s" % (level, msg))
        failed = failed or bool(r.errors)
    if hidden:
        print("(%d convention warnings on older posts hidden; add -v to see them)" % hidden)
    print("\nRESULT: %s" % ("FAILED - fix every ERROR and re-run" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
