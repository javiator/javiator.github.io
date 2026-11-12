# Site structure

Jekyll site on GitHub Pages using the Minimal Mistakes theme (`remote_theme`, skin `air`). Pushing to `main` deploys it to https://blog.architectureon.co.uk. GitHub Pages builds with its own gem set and ignores the repo `Gemfile`; custom plugins are not available.

## Where things live

| Path | What it is |
|------|------------|
| `_posts/YYYY/MM/YYYY-MM-DD-<slug>.md` | Posts. Posts from 2025 sit directly in `_posts/`; leave them there. |
| `assets/images/posts/YYYY/MM/<slug>/` | All files for a post: images, `header.png`, and any self-hosted embed such as a slide deck (`deck.html`, shown in the post with an `<iframe>`). Older posts use `assets/images/headers/` and `assets/images/<project>/`. |
| `_data/series.yml` | Series definitions (id, title, description, icon, tags, status). |
| `_pages/series/<id>/index.md` | One landing page per series. |
| `_data/projects.yml`, `_data/evolutions.yml` | Projects and their numbered evolutions. |
| `_pages/projects/<project-id>/` | Project overview, `posts/` timeline, and one `evolution-N/` page per evolution. |
| `_includes/evolution/` | Components for project pages and posts. `posts-list.html` generates every list of project posts. |
| `_layouts/single.html`, `_includes/sidebar.html`, `_includes/head/custom.html` | Local overrides of the theme: layout, sidebar with recent posts, Mermaid and analytics loading. |
| `index.md`, `_pages/projects.md`, `_pages/series.md` | Home, Projects, and Series pages. |
| `_data/navigation.yml` | Top navigation. |
| `.claude/skills/new-blog-post/` | This skill: conventions, template, validator, preview. |

## The three kinds of post

1. **Standalone**: no `series`, no `project`. Listed under "Standalone Articles" on the home and Projects pages.
2. **Series post**: has `series: <id>` and `series_order`. Listed on `/series/<id>/` and counted on `/series/`. Series so far: see `validate_post.py --taxonomy`.
3. **Evolution post**: belongs to a project built up in numbered evolutions. Has `project`, `project_type`, `evolution`, `evolution_number`, `evolution_focus`, and ends with two includes. The only project is Tenant Management, and all six of its evolutions are marked complete, so a new evolution post needs either an existing evolution to belong to or a new evolution approved by the author.

A series post has no `project` fields. In the home and Projects pages "standalone" means "no `project`", so series posts also appear there; that is expected.

## Front matter

Site defaults in `_config.yml` already give every post `layout: single`, the author profile, reading time, sharing, related posts, and a sticky table of contents. Do not repeat them.

Every new post has:

| Key | Rule |
|-----|------|
| `title` | One line. Quote it. |
| `date` | `YYYY-MM-DD`, same as the filename. A future date is not published until that day. |
| `permalink` | `/<category-1>/<category-2>/.../<slug>/`, all kebab-case. Always set it: without it, categories containing spaces or capitals produce awkward URLs. |
| `categories` | Two or three, from `taxonomy.yml`: one primary first, then one or two topics. They form the URL. |
| `tags` | Four to ten, kebab-case. Reuse existing tags where one fits. |
| `excerpt` | One or two sentences. Used on listings, archives, project and series pages. |
| `content_type` | One value from `taxonomy.yml`. |
| `learning_focus` | List of kebab-case topics. |
| `difficulty` | `beginner`, `intermediate`, or `advanced`. |
| `header` | `overlay_image`, `overlay_filter: 0.5`, and `teaser` (same image as the overlay). |

Optional: `featured: true` puts the post in the home page's Featured list. `mermaid: true` is required when the body has Mermaid blocks and should be absent otherwise.

Series posts add `series` and `series_order`. Evolution posts add:

```yaml
project: "Tenant Management"          # the project's title-case name; its id is the kebab-case form
project_type: "evolutionary"
evolution: "Evolution 6: Cloud Deployment Strategies"   # "Evolution N: <title in _data/evolutions.yml>"
evolution_number: 6
evolution_focus: "Cloud Deployment Strategies"
```

and end the body with exactly:

```liquid
{% include evolution/evolution-posts.html %}
{% include evolution/post-navigation.html %}
```

Do not use `feature`, `description`, or `image`: they were typos or duplicates of `featured` and `excerpt`.

## What updates itself

Adding a post file is enough for all of these:

- Home page: recent posts, featured, standalone list, post counts
- `/posts/`, `/categories/`, `/tags/` archives, sidebar "Recent Posts", related posts, feed, sitemap
- `/series/` counts and each `/series/<id>/` list
- Projects page "All Posts by Evolution", each evolution page's "Posts in This Evolution", the project's `/posts/` timeline and summary table, and the cards at the foot of each evolution post

## What to update for each kind of post

**Standalone post, or a post in an existing series or existing evolution**: nothing beyond the post and its images.

**New series** (needs the author's approval):

1. Add an entry to `_data/series.yml` with `title`, `description`, `icon`, `tags`, and `status: "active"`.
2. Create `_pages/series/<id>/index.md` by copying an existing series page and replacing the id (it appears three times), title, icon, and introduction.

Three series exist with no posts yet (`aws-journey`, `python-mastery`, `react-patterns`); prefer one of them over creating a near-duplicate.

**New evolution in an existing project** (needs the author's approval):

1. Add the evolution to `_data/evolutions.yml` (`number`, `title`, `status`, `focus`, `technologies`, `url`).
2. Create `_pages/projects/<project-id>/evolution-N/index.md` by copying the latest one. Keep the `posts-list.html` include; rewrite the overview, objectives, achievements, and learnings.
3. Update the hand-written prose that names evolutions:
   - `_pages/projects/<project-id>/index.md`: the Mermaid journey diagram, and "Learning Journey".
   - `_pages/projects/<project-id>/posts/index.md`: "Learning Journey Highlights" and "Project Statistics".
   - `_pages/projects.md`: the evolution summary near the top, "Quick Links", and "Content Overview".
   - `index.md`: the "Featured Project" block ("Current Evolution", technologies).
4. If the evolution reopens a finished project, set the project's `status` in `_data/projects.yml` and the evolution's `status` accordingly.

**New project**: a larger change that adds a project to both data files, a set of pages mirroring `_pages/projects/tenant-management/`, and a section on `_pages/projects.md`. Several pages currently name `tenant-management` directly. Plan it with the author before starting.

**Changing an evolution's status**: `_data/evolutions.yml` drives the status badges; check the prose in the files listed above still agrees.

## Things that break the build or the page

- Liquid syntax in prose or code samples that is not wrapped in `{% raw %}`.
- A `/` inside a category name (creates nested URL segments).
- Mermaid blocks without `mermaid: true`, or Mermaid syntax errors (shown as an error graphic on the page).
- Image paths that do not exist. Paths are absolute from the site root: `/assets/images/...`.
- An H1 in the body: the theme already renders the title, and the table of contents nests under it.
- Two posts with the same slug or URL.

## Local build

`scripts/preview.sh` builds with its own `Gemfile` and `_config.preview.yml` next to it, which swap the remote theme for the equivalent gem so the build works offline from GitHub. The repo-root `Gemfile` pins an old Jekyll that does not run on current Ruby; it is not used by GitHub Pages or by this skill.
