---
name: plotline-diagrams
description: Create architecture and flow diagrams as Plotline YAML files and render them to SVG for a blog post, README or document. Use when asked for a diagram of a system, a pipeline, a request flow or a step-by-step walkthrough, especially in a Jekyll or other static site where a picture file is embedded in Markdown.
---

# Plotline diagrams

A Plotline diagram is a small YAML file, `name.diagram.yaml`. It says what is in the picture; the layout is automatic. The `plotline` command in this skill checks the file and renders it to an SVG that needs no script on the page.

Run the command with Node 18 or newer:

```
node <this skill's folder>/scripts/plotline.js <command>
```

It reads and writes local files only.

## Steps

1. **Write** `name.diagram.yaml` next to where the picture is wanted (see the format below). Keep the YAML: it is the source, and the picture is regenerated from it.
2. **Look up types** rather than guessing them: `plotline.js types queue` lists matching node types; `plotline.js types` lists all of them.
3. **Validate**: `plotline.js validate name.diagram.yaml`. Fix every `error` line and run it again until it prints `valid`.
4. **Render**: `plotline.js render name.diagram.yaml --out <folder>`. It prints the path of each file it wrote.
5. **Embed** the SVG in the post (see "In a Jekyll post").

Never write the SVG by hand, and never edit a rendered SVG: change the YAML and render again.

## The format

```yaml
version: 1                    # always 1
title: Online shop
direction: right              # right (default) or down

groups:                       # optional: boxes around nodes; may nest with parent
  backend:
    label: Backend
    type: boundary            # a group type from `plotline.js types`

nodes:
  shopper:                    # the id: lower-case letters, digits, hyphens; unique across nodes and groups
    type: user                # a node type from `plotline.js types`; decides the icon and colour
    label: Shopper            # shown on the card; keep it to three words or fewer
  api:
    type: api
    label: Shop API
    parent: backend           # puts the node inside a group
  db:
    type: database
    label: Orders
    parent: backend
    description: Postgres, one primary

edges:
  - from: shopper
    to: api
    label: HTTPS              # optional; one or two words
  - from: api
    to: db
    style: dashed             # solid (default), dashed or dotted; use dashed for asynchronous
    arrow: forward            # forward (default), both or none

flows:                        # optional: walkthroughs, played one step at a time
  - id: checkout
    title: Placing an order
    steps:
      - from: shopper         # a step travels along an existing edge, in either direction
        to: api
        note: The shopper presses Buy.
      - from: api
        to: db
        note: The order is saved.
        duration: 3           # seconds this step stays on screen; default 2.5
      - highlight: [db]       # a step may instead just light up nodes or groups
        note: The order is now durable.
```

Rules that validation enforces:

- Every `from`, `to`, `parent` and `highlight` must name something that exists.
- A step's `from` and `to` must be joined by an edge.
- An edge without an `id` is known as `<from>--<to>`; give edges an `id` only when two edges join the same pair.
- No coordinates anywhere. Do not try to place things.

Writing a diagram that reads well:

- 5 to 12 nodes. Split a bigger system into two diagrams.
- Group by what a reader recognises (a network, a team, a stage), at most two levels deep.
- `direction: right` for pipelines and request paths; `direction: down` for layered architectures.
- Label an edge only when the label says something the two ends do not.
- A walkthrough of 3 to 6 steps, each note one plain sentence.

## Rendering

```
plotline.js render shop.diagram.yaml                               # shop.svg beside the YAML
plotline.js render shop.diagram.yaml --out assets/diagrams/        # into a folder
plotline.js render shop.diagram.yaml --theme dark --out assets/diagrams/shop-dark.svg
plotline.js render shop.diagram.yaml --format flow-svg --out assets/diagrams/
        # one animated SVG per walkthrough: shop-checkout.svg. Plays by itself and loops.
plotline.js render shop.diagram.yaml --format flow-player --out _includes/diagrams/
        # one HTML snippet per walkthrough, with play, pause and step buttons: shop-checkout.html
plotline.js render shop.diagram.yaml --format flow-html --flow checkout
        # a page with one picture and caption per step
plotline.js render shop.diagram.yaml --format mermaid              # Mermaid text, without icons or walkthroughs
```

Sizes: a still SVG is about 3 to 10 KB, an animated one or a player snippet about 15 to 25 KB. The player script is under 5 KB.

## In a Jekyll post

Keep the YAML and the SVG together, for example in `assets/diagrams/`, and commit both.

```markdown
![Online shop: the shopper calls the Shop API, which saves orders in a database]({{ '/assets/diagrams/shop.svg' | relative_url }})
```

- Write alt text that says what the diagram shows, not "diagram".
- Use `<img>` or Markdown image syntax for still pictures, not inline SVG pasted into the post.
- If the site has a dark mode, render both themes and let the browser choose:

```html
<picture>
  <source srcset="{{ '/assets/diagrams/shop-dark.svg' | relative_url }}" media="(prefers-color-scheme: dark)">
  <img src="{{ '/assets/diagrams/shop.svg' | relative_url }}" alt="Online shop: …">
</picture>
```

### A walkthrough the reader can step through

Prefer this for walkthroughs. The reader gets play, pause, next, previous and restart; without JavaScript (or in a feed reader) they get the diagram and the steps as a numbered list.

1. Once per site, write the player script and load it from the layout:

   ```
   plotline.js player --out assets/js/
   ```

   ```html
   <script defer src="{{ '/assets/js/plotline-player.js' | relative_url }}"></script>
   ```

   Check whether the layout already loads it before adding it again.

2. Render the walkthrough into `_includes`:

   ```
   plotline.js render assets/diagrams/shop.diagram.yaml --format flow-player --out _includes/diagrams/
   ```

3. Put it in the post on a line of its own, with a blank line before and after:

   ```liquid
   {% include diagrams/shop-checkout.html %}
   ```

The snippet's colours are fixed when it is rendered: pass `--theme dark` for a dark site. Do not edit the snippet; render it again.

If the page cannot run scripts at all, use `--format flow-svg` instead and embed it as an image: it plays by itself and loops, but cannot be paused, so put the steps in the text too.

## When something goes wrong

- `error:` lines from `validate` name the file and line. Fix the YAML; do not work around it.
- `Nothing was rendered` means the file has errors: validate first.
- A label cut short with `…` is too long for its card: shorten the label and move detail into `description` or the post's text.
