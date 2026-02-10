---
layout: single
title: "Agentic AI: Capability vs Architecture"
date: 2026-02-10
categories: [Concepts, Fundamentals, AI/ML, Architecture]
tags: [agentic-ai, multi-agent-systems, architecture, patterns]
series: "agentic-systems"
description: "Demystifying the difference between Agentic AI (a capability) and Multi-Agent Systems (an architecture) using a simple kitchen analogy."
image: 
mermaid: true 
---

## Introduction

"Agentic AI" is the buzzword of the moment. It's everywhere in my feed, often accompanied by complex diagrams of five different bots talking to each other to accomplish a task. But there is a growing pattern of confusion: smart people are equating "Agentic AI" solely with these complex "Multi-Agent Systems" (MAS).

It’s time to clear up the confusion. Agentic AI is a **capability**, while Multi-Agent Systems are just one specific **architecture** for achieving it.

> [!IMPORTANT]
> A single, well-orchestrated LLM loop that can plan, act, and observe is 100% Agentic AI. You don't always need a squad to be agentic.

## What is it?

At its core, **Agency** refers to the capability of a system to be autonomous. It's not about how many models are running; it's about what the system can *do*.

An Agentic system isn't just a passive chatbot waiting for a prompt. It has a loop:
1.  **Understand** a high-level goal.
2.  **Formulate** a plan.
3.  **Use Tools** (search the web, run code, query a database).
4.  **Observe** the results and **Correct** its own mistakes.

If a single script running one LLM can do this loop, it is an agent.

## Why does it matter?

We need to stop using "Agentic" and "Multi-Agent" interchangeably because it leads to over-engineering.

*   **The Capability**: A system that can autonomously plan, use tools, and achieve a goal.
*   **The Architecture**: Assigning those tasks to a squad of specialized bots vs. one generalist.

If you assume you need a "Multi-Agent System" to be "Agentic," you might build a complicated system when a simple loop would have sufficed.

## How it works

To understand the difference, let's visualize it with a kitchen analogy: **The Brain vs The Room**.

### The Single Agent: The Master Chef

Imagine a Master Chef in a small, high-end kitchen. They are **autonomous**, **capable**, and **self-correcting** (planning, cooking, tasting). They carry all the context in their head and can switch tasks rapidly.

### The Multi-Agent System: The Kitchen Brigade

Now imagine a huge hotel kitchen with specialized chefs (Sauce, Grill, Pastry) and an Expeditor. This is a **Multi-Agent System**. It's powerful for massive operations but comes with communication overhead.

| Kitchen Role | Technical Equivalent | Function |
| :--- | :--- | :--- |
| **Sauce Chef** | **Database Agent** | Accesses internal SQL/Vector DBs. |
| **Grill Chef** | **Coder Agent** | Generates and executes Python/JS code. |
| **Expeditor** | **Orchestrator** | Routes tasks, manages state, and ensures the final JSON is valid. |

<div class="mermaid">
flowchart LR
    subgraph SingleAgent ["Single Agent Loop (The Master Chef)"]
        direction TB
        Goal(Goal) --> Plan(Plan)
        Plan --> Act
        
        subgraph ActionLoop [Execution Loop]
            direction TB
            Act(Act) --> Tool[Tool Use]
            Tool --> Result(Result)
            Result --> Observe{Observe}
            Observe -->|Incomplete/Error| Correct(Self-Correct/Re-Plan)
            Correct --> Act
        end
        
        Observe -->|Success| Finish(((Finish)))
    end

    subgraph MultiAgent ["Multi-Agent System (The Brigade)"]
        direction TB
        M[Manager Agent] <-->|Task| W1[Writer Agent]
        M <-->|Code| W2[Coder Agent]
        M <-->|Review| W3[Reviewer Agent]
        W2 -.->|Chatter| W3
    end

    style SingleAgent fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    style MultiAgent fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    style ActionLoop fill:#ffffff,stroke:#2196f3,stroke-dasharray: 5 5
</div>

### The Soft Boundary: Persona Switching

There is a powerful middle ground called **Persona Switching**. Instead of multiple agents, you use **one agent** but dynamically swap its system prompt during the loop (e.g., "Act as Planner" -> "Act as Coder" -> "Act as Reviewer"). This is the "Sweet Spot" for 80% of use cases.

## Examples

### 1. The "Web Scraper" Loop (Single Agent Capability)
Imagine finding a product price:
1.  **Loop 1 (Plan)**: Search Google.
2.  **Loop 2 (Act)**: Scrape URL. *Result: 403 Forbidden*.
3.  **Loop 3 (Observe & Correct)**: Switch to headless browser tool.
4.  **Loop 4 (Success)**: Extract price.
*Agency is the loop, not the number of bots.*

### 2. The Context Wall (When to use Multi-Agent)
You need to summarize 50 long PDF contracts. A single agent's context window will choke.
*   **Solution**: Split it. Agent A (Researcher) searches and summarizes PDFs. Agent B (Writer) takes summaries and writes the report.

### 3. The Instruction Wall (When to use Multi-Agent)
Your prompt is 3,000 words long trying to teach one model to be a Lawyer, Coder, and Poet. It forgets rules.
*   **Solution**: Split prompts. dedicated "Coder Agent" and "Reviewer Agent".

## Conclusion

Don't fall into the trap of over-engineering. Start with the **Master Chef** (Single Agent). Build the **Brigade** (Multi-Agent) only when the kitchen gets too chaotic.

**What about you?** Are you finding yourself building squads when a single agent would do?
