# Blog repo guide

Personal blog: Jekyll + Minimal Mistakes on GitHub Pages, deployed from `main` to https://blog.architectureon.co.uk.

- **Writing or editing a post**: use the `new-blog-post` skill (`.claude/skills/new-blog-post/SKILL.md`). It holds the conventions, a validator, and a preview script.
- **How the site is organised**, what updates itself, and what must be edited by hand: `.claude/skills/new-blog-post/site-structure.md`. Read it before changing pages, data files, or includes.
- Lists of posts are always generated with Liquid. Never hand-write a list of posts into a page.
- Never change the `categories`, `permalink`, date, or slug of a published post: it changes the URL.
- Check any change with `.claude/skills/new-blog-post/scripts/validate_post.py --all` and `.claude/skills/new-blog-post/scripts/preview.sh --build-only`.
- Work on a branch; do not push to `main` directly.
