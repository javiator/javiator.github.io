---
name: new-blog-post
description: Create a new blog post for this Jekyll site from a topic, a PDF, notes, or ready-made material. Maps the post onto the site's structure (standalone, series, or project evolution), asks the author a small set of clarifying questions with recommendations, writes the post and its assets, updates every related listing, validates it, and produces a rendered preview (PNG + PDF) for review. Use whenever the author asks to write, draft, add, or publish a blog post, or to turn material into a post.
---

# New blog post

The author wants to hand over a topic or material and get back a post that is correct first time: right place, right front matter, every listing updated, and a rendered preview to review. Past attempts failed because the model guessed at the site's structure. Do not guess: everything you need is in `site-structure.md`, `taxonomy.yml`, and the output of the scripts below. Read `site-structure.md` now, before anything else.

All paths below are relative to the repo root. `SK` means `.claude/skills/new-blog-post`.

## 1. Take in the material

Read everything the author supplied, in full: PDFs, documents, images, links, pasted notes. If they gave only a topic, the post is written from your own knowledge plus anything they add, so say that in step 3 and ask what angle or experience of theirs it should carry.

Images and diagrams supplied by the author are content, not decoration: plan where each one goes.

## 2. Read the current state of the site

Run:

```bash
python3 SK/scripts/validate_post.py --taxonomy
```

This prints the allowed categories, the tags already in use, every series with its next `series_order`, and every project evolution. Then read the two or three existing posts closest to the new one (same series, same evolution, or same topic) so the new post matches their voice and can link to them.

## 3. Decide, then ask once

Work out a complete proposal yourself first. Then ask the author only what you cannot settle from the material, in a single round of questions, each with a recommended answer first and a one-line reason. Typical questions:

- **Placement**: standalone, part of an existing series, a new series, or a project evolution post. Recommend one.
- **Title**: two or three options.
- **Angle and audience** when the material supports more than one.
- **Header image**: author supplies one, generate an abstract one, or reuse an existing header.
- **Date** if it should not be today, and whether it should be `featured`.

Do not ask about things with a clear answer (categories, tags, content type, difficulty, slug, file paths): choose them, and list your choices in one short block alongside the questions so the author can correct any of them. If the author has already answered something in their request, do not ask it again.

Anything that adds to the site's structure needs explicit approval, because it changes more than one post: a new series, a new evolution or project, or a new category or content type in `taxonomy.yml`.

## 4. Write the post

Start from `SK/templates/post.md`. The rules that matter are in `site-structure.md` under "Front matter" and are enforced by the validator, so the template plus the validator will keep you right.

On the writing itself:

- The author writes in the first person, in British English, as a practising architect explaining something they worked through. Posts open with the problem or question, use an analogy or concrete example early, and end with a conclusion or key takeaways. Match the neighbouring posts you read in step 2 rather than a generic blog voice.
- Stay faithful to the source material. Do not add figures, benchmarks, quotes, or claims about the author's own experience that the material does not contain. Where the material has a gap the post needs filled, either ask or leave it out, and tell the author in your final report.
- Use H2 for sections and H3 beneath; never an H1. Separate major sections with `---` as existing posts do.
- Use tables for comparisons. For architecture and flow diagrams use the `plotline-diagrams` skill, not Mermaid (see "Diagrams" in step 5). Older posts use Mermaid; leave those as they are.
- Link to related posts on this site by their published URL (`validate_post.py --url <file>` prints it). Do not invent URLs.
- Liquid syntax (`{{ }}` or `{% %}`) in prose or code samples must be wrapped in `{% raw %}...{% endraw %}`, or the build breaks.

## 5. Add the assets

All of a post's images go in `assets/images/posts/YYYY/MM/<slug>/`. Use kebab-case filenames and give every image alt text.

For the header (`header.png` in that folder), in order of preference: the author's image; a generated one; a reused existing header only if the author chose that.

```bash
node SK/scripts/make_header.js assets/images/posts/YYYY/MM/<slug>/header.png "<slug>" [hue]
```

It draws an abstract background with no text, since the theme overlays the title. Pick a hue that suits the topic if the default clashes.

**Diagrams.** Follow the `plotline-diagrams` skill (`.claude/skills/plotline-diagrams/SKILL.md`). Keep each `name.diagram.yaml` in the post's asset folder and render next to it:

```bash
PL="node .claude/skills/plotline-diagrams/scripts/plotline.js"
$PL validate assets/images/posts/YYYY/MM/<slug>/name.diagram.yaml
$PL render   assets/images/posts/YYYY/MM/<slug>/name.diagram.yaml --out assets/images/posts/YYYY/MM/<slug>/
```

- A still diagram is embedded as a Markdown image with alt text that says what it shows.
- A step-by-step walkthrough is rendered with `--format flow-player --out _includes/diagrams/` and placed with `{% include diagrams/<name>-<flow id>.html %}` on a line of its own. The player script is already loaded on every page from `_includes/head/custom.html`.
- The post column is about 700px wide. A wide row of cards becomes unreadably small, so prefer `direction: right` with grouped nodes (they stack vertically) or `direction: down` for a chain of decisions, and look at the result in the preview.
- The caption under each card is the type's name ("LLM", "Step", "Storage"), so pick a type whose name is not misleading. Labels longer than about 16 characters are cut short.
- Commit the YAML with the rendered files; never edit a rendered SVG or snippet.

To embed something interactive (a slide deck, a demo), self-host it as a single self-contained HTML file in the same folder and show it with an `<iframe>` in a 16:9 wrapper, plus a link that opens it in its own tab. `_posts/2026/11/2026-11-12-agentic-orchestration-patterns.md` is the reference example. Do not embed pages from other sites unless the author confirms they allow framing.

## 6. Update everything related

Listings of posts are generated automatically. What is not automatic depends on placement; follow the matching checklist in `site-structure.md` ("What to update for each kind of post"). Never hand-write a list of posts into a page.

## 7. Validate

```bash
python3 SK/scripts/validate_post.py <path to the new post>
```

Fix every `ERROR` and re-run until the result is `OK`. Read each `WARN` and `NOTE` and either fix it or be ready to explain it; a `NOTE` about new tags means you should check an existing tag would not do.

Then run `python3 SK/scripts/validate_post.py --all` to confirm nothing else broke.

## 8. Preview

```bash
SK/scripts/preview.sh <path to the new post>
```

This builds the whole site, renders the post in a headless browser, checks images, diagrams, internal links, and that the post appears on every listing it should, and writes to `.preview/`:

- `<slug>.png`: full-page desktop render
- `<slug>-mobile.png`: top of the page at phone width
- `<slug>.pdf`

Fix every `ERROR` and re-run. Then look at the PNG yourself before showing it to anyone: check the hero image and title are legible, diagrams are readable and not clipped, tables fit, and nothing looks like leftover template text. Fix what you find and re-run.

If the script cannot run in your environment (no Ruby or no Playwright), say so plainly rather than claiming the post was previewed.

## 9. Hand over

Send the author the PNG and PDF, and report briefly:

- where the post lives and its URL
- the placement, categories, and tags you chose
- which other files you changed and why
- anything you left out, were unsure of, or want them to check

Do not commit until the author has reviewed the preview, unless they asked you to. When committing, work on a branch and never push to `master` directly; the site deploys from `master`.

## Editing an existing post

The same steps 7 and 8 apply. Do not change the `categories`, `permalink`, filename date, or slug of a published post: that changes its URL and breaks inbound links.
