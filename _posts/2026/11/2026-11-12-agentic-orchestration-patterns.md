---
title: "Agentic Orchestration: Twelve Patterns and When Each One Earns Its Cost"
date: 2026-11-12
permalink: /concepts/ai/architecture/agentic-orchestration-patterns/
categories: [Concepts, AI, Architecture]
tags: [ai, agents, agentic-ai, orchestration, patterns, architecture, multi-agent-systems, llm]
excerpt: "Orchestration is the set of ways to combine model calls, tools and code so the result beats a single prompt. A map of twelve patterns, split by one question: who decides the next step, your code or the model?"
content_type: "concept-deep-dive"
learning_focus: ["agentic-orchestration", "workflow-patterns", "agent-patterns", "guardrails", "evaluation"]
difficulty: "intermediate"
series: "agentic-systems"
series_order: 4
header:
  overlay_image: /assets/images/posts/2026/11/agentic-orchestration-patterns/header.png
  overlay_filter: 0.5
  teaser: /assets/images/posts/2026/11/agentic-orchestration-patterns/header.png
---

"Orchestration" has become one of those words that means whatever the nearest framework says it means. Supervisors, routers, planners, reflection loops, swarms: each comes with its own diagram, and it is hard to tell which of them are different ideas and which are the same idea with a new name.

To get past the vocabulary I built the [Agentic Orchestration Playground](https://github.com/javiator/agentic-orchestration-play): twelve small, runnable exercises, each showing one pattern with real models and a page that streams every step. This post is the map that came out of it, with the slide deck embedded below so you can step through each pattern.

**The short version:** orchestration is the set of ways to combine model calls, tools and code so the result is better than one prompt would give you. Almost every pattern falls on one side of a single question: *who decides the next step, your code or the model?*
{: .notice--info}

---

## The deck

Thirty-one slides: the map, then two slides per pattern (the problem it solves and when to skip it, then how it works and what to take away). Use the arrows, click, swipe, or press the arrow keys once you have clicked inside it.

<div style="position:relative;width:100%;aspect-ratio:16/9;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.25);background:#0d1324;">
  <iframe src="/assets/images/posts/2026/11/agentic-orchestration-patterns/deck.html" title="Agentic Orchestration: Twelve Patterns (slide deck)" loading="lazy" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
</div>

[Open the deck in its own tab](/assets/images/posts/2026/11/agentic-orchestration-patterns/deck.html){: .btn .btn--primary}

---

## One question splits the field

In [the first post of this series](/concepts/fundamentals/ai/ml/architecture/agentic-ai-capability-vs-architecture/) I used a kitchen to separate agentic capability from multi-agent architecture. The same kitchen works here.

A **workflow** is a recipe card. The steps are written down in advance, and the cook follows them. A model may do the work at each step, but your code decides what happens next.

An **agent** is the chef tasting the sauce and deciding what it needs. The model looks at the result so far and chooses the next action itself.

Neither is better. The recipe card is predictable, cheap and easy to test. The chef copes with dishes nobody wrote a recipe for, and you pay for every decision.

![The orchestration map: one question, who decides the next step, splits eight patterns into workflows (prompt chain, router, consensus, reflection loop) and agents (supervisor, planner, agentic RAG, code agent); four controls wrap around all of them: human-in-the-loop, guardrails, context management and an eval harness](/assets/images/posts/2026/11/agentic-orchestration-patterns/orchestration-map.svg)

Eight patterns sit on one side or the other. The remaining four are not alternatives to them: they are the controls you wrap around whichever pattern you pick.

---

## Workflows: code decides the steps

| Pattern | What it does | Use it when | Skip it when |
|---------|--------------|-------------|--------------|
| **Prompt chain** | Small steps with code checks between them, instead of one big prompt | The task splits into known steps and code can check the output | A strong model already gets it right in one shot |
| **Router** | A cheap model reads each request and picks the path, and the price, for it | Traffic is mixed: many easy requests, some hard | Every request is hard, or a misroute is costly and hard to detect |
| **Consensus** | Several models answer independently; a judge merges them and flags disagreements | The question is high-stakes or contested and you want to know how sure to be | It is a simple lookup, or latency and cost matter more than confidence |
| **Reflection loop** | Draft, critique, revise until good enough, no longer improving, or out of budget | Quality matters and the criteria are clear and checkable | The first draft is usually fine, or the critic cannot judge better than the writer |

A few things stood out when running these.

**Code gates are the cheapest quality control there is.** In the prompt chain, the outline comes back as JSON and code checks it before anything else runs. A check written in code is free, instant and exact, so check everything you can that way, and when a check fails, repair only what failed rather than regenerating the lot.

**A router is a model too.** Most traffic is easy, so one small routing call can save many large ones. But the router can be wrong, which is why it returns a confidence score and escalates to the stronger path when unsure. A wrong cheap answer usually costs more than the upgrade would have.

**Disagreement is signal.** In the consensus pattern, the judge does not just merge three answers; it attributes each claim to a model and lists where they differ. Those differences show exactly where to double-check. And because the fan-out is parallel, three models take about as long as the slowest one.

**Reflection has diminishing returns.** Most of the gain comes in the first round; later rounds cost the same and add little. Who critiques matters as well: a model grading its own work is generous, an independent critic is stricter. Keep the best-scoring version, not the last, because a revision can make things worse.

---

## Agents: the model decides the steps

| Pattern | What it does | Use it when | Skip it when |
|---------|--------------|-------------|--------------|
| **Supervisor and specialists** | A supervisor model decides, turn by turn, which specialist acts next and when the job is done | The goal is open-ended and sub-tasks need different skills | The steps are predictable (use a workflow), or budgets are tight |
| **Planner and executor** | Plans the whole job as a graph up front, runs independent steps in parallel, replans on failure | The work is multi-part and you want parallelism and a readable plan | Each step depends on surprises in the last |
| **Agentic RAG** | Search becomes a tool: the model writes its own queries and checks its answer is grounded | Questions are multi-hop or worded differently from the documents | It is a one-fact lookup; plain RAG is far cheaper |
| **Code-executing agent** | The model writes Python, runs it, reads the output or traceback, and fixes its code | You need exact computation over data: counting, dates, tables | Users are untrusted and you have no real sandbox |

**The supervisor is simpler than its diagrams suggest.** Each specialist is exposed to the supervisor as a tool. The supervisor's own reason-and-act loop is the orchestrator: it delegates, reads the result, and decides again. What keeps it honest is plain engineering: a cap on turns, and a block on repeating the same delegation, so a confused supervisor cannot spin for ever.

**A planner trades flexibility for fewer decisions.** One planning call produces the steps and their dependencies, code validates the graph (ids, dependencies, no cycles), and independent steps run in parallel waves. The price is that it commits early, so a failed step needs an explicit replan, one that keeps the finished work and plans only what is left.

**Agency in retrieval is worth it for some questions and wasteful for others.** An agent can follow a lead that the first search revealed, which a fixed retrieve-then-answer pipeline cannot. It also costs several times the calls and latency. For questions the documents cannot answer, "the documents don't say" is the correct response from either approach.

**A traceback is better feedback than a critique.** Models are unreliable at arithmetic and at reading large tables, but good at writing code that does both. When that code fails, the error is real feedback from the world rather than another model's opinion. The sandbox in the playground is a teaching device; a real deployment needs proper isolation such as containers or virtual machines.

---

## Around every pattern

These four apply whichever of the eight you choose.

| Control | The problem it addresses | The idea |
|---------|--------------------------|----------|
| **Human-in-the-loop** | Full autonomy is dangerous for irreversible actions; approving everything makes people the bottleneck | Gate by risk: routine actions run, irreversible ones wait |
| **Guardrails** | A prompt instruction is a request, not a control | Layer checks on input and output, cheapest first |
| **Context management** | Conversations outgrow what is cheap, or possible, to send | Choose deliberately what the model gets to remember |
| **Eval harness** | Eyeballing a few answers is how bad patterns ship | Same questions, every option, side by side |

**Gate by risk, not by default.** In the human-in-the-loop exercise a policy written in code checks every tool call. Reads and small refunds run immediately; large refunds and external emails pause for a person, who can approve, edit, or reject with feedback. The feedback matters: it goes back into the conversation, so the agent adapts instead of retrying the same thing. Real systems also checkpoint the paused state so that a pause survives a restart.

**Instructions are not controls.** The guardrails exercise runs the same support bot twice, with a confidential discount code in its prompt. The unguarded copy gives it up to a simple pretext. The guarded copy is wrapped in layers ordered from cheap to expensive: code checks first, model checks only when needed, on the way in and on the way out. Every layer trades false positives against leaks, so measure both.

**Memory is a design decision.** Sending the full history gives the best recall at a cost that grows every turn. A sliding window is cheap and forgets everything outside it, completely. A running summary keeps the gist and loses specifics. Notes keep the specific facts and can update one that changes.

**Measure, don't eyeball.** A pattern that costs five times the calls has to earn it. The eval harness runs single-model baselines and the patterns over the same questions and reports quality, latency and cost together. Two cautions: the grader is itself a model with biases, so read its reasons and not just its scores; and small question sets are noisy, so one question can swing an average.

---

## Choosing a pattern

The order I would work through, starting from the cheapest option. Press play to follow one open-ended task through it, or step through at your own pace:

{% include diagrams/choosing-a-pattern-walkthrough.html %}

This is the same argument as [How Much AI Should We Use?](/concepts/architecture/ai/how-much-ai-should-we-use/), one level down: every extra model call should buy something, and you should be able to say what.

---

## Does the map still hold?

I put this material together as a set of lessons, so before publishing I checked it against how the patterns are described elsewhere today.

**The core split holds.** Separating workflows, where code controls the path, from agents, where the model does, is the framing Anthropic set out in [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), and the guides I looked at still build on it. The advice that goes with it has not changed either: start with the simplest thing that works and add agency only where it pays.

**Some labels are a judgement call.** Where a pattern sits depends on which question you ask. I have put the planner under agents because a model writes the plan. Others file plan-then-execute and orchestrator-style delegation under workflows, because once the plan exists, code runs it. Both readings are defensible; what matters is knowing which decisions the model makes and which your code makes. The same pattern also travels under different names: reflection is often called evaluator-optimiser, and consensus is a form of parallelisation with voting.

**Three things the map does not cover.** They are not patterns in the same sense, but you will meet them as soon as these systems leave the playground:

- **How agents connect to tools and to each other.** I covered that separately in [When to Use MCP vs. Agent Skills](/concepts/fundamentals/ai/ml/agentic-connectivity-mcp-vs-agent-skills/).
- **Handoffs between agents.** The supervisor exercise shares a scratchpad between specialists. In larger systems, deciding how much context crosses each boundary becomes a design problem of its own.
- **Observability.** The playground streams every step to the page. A production system needs the equivalent as tracing, so you can see which call made which decision after the fact.

---

## Conclusion

Orchestration is less exotic than the diagrams make it look. There are a handful of ways to arrange model calls, and one question sorts them: does your code decide the next step, or does the model?

- **Prefer the simplest pattern that works**: a single call before a workflow, a workflow before an agent.
- **Check in code whatever code can check.** It is free, instant and exact.
- **Put guards on every loop**: turn caps, repeat blocks, budgets.
- **Wrap whatever you build** in approvals for risky actions, layered guardrails and deliberate context management.
- **Measure before you believe it.** The right pattern is the cheapest one that passes your evals.

The quickest way to make any of this stick is to break it: run the [playground](https://github.com/javiator/agentic-orchestration-play), change a prompt, swap a model, lower a limit, and watch what happens.
