---
title: "Knowledge in Agentic Apps: How AI Agents Find What They Know"
date: 2026-11-13
permalink: /concepts/ai/architecture/knowledge-in-agentic-apps/
categories: [Concepts, AI, Architecture]
tags: [ai, agents, agentic-ai, rag, knowledge-management, mcp, llm, architecture]
excerpt: "A model knows the world, not your organisation. How agents are grounded in your own data: RAG, hybrid search, knowledge graphs, agentic retrieval and memory, and how Microsoft 365 Copilot applies the same patterns at the scale of a whole tenant."
content_type: "concept-deep-dive"
learning_focus: ["retrieval-augmented-generation", "hybrid-search", "knowledge-graphs", "agentic-retrieval", "agent-memory"]
difficulty: "intermediate"
series: "agentic-systems"
series_order: 5
header:
  overlay_image: /assets/images/posts/2026/11/knowledge-in-agentic-apps/header.png
  overlay_filter: 0.5
  teaser: /assets/images/posts/2026/11/knowledge-in-agentic-apps/header.png
---

Ask a capable model about your leave policy and it will answer fluently and wrongly. It has read a large slice of the internet, but it has never seen your contracts, your HR site or last week's meeting notes. Everything an agent does well inside an organisation depends on how it gets hold of that knowledge.

I put together a visual guide to the patterns behind this, from plain retrieval to agentic loops and memory, with Microsoft 365 Copilot as the worked example of all of them running at scale. This post walks through it, with the deck embedded below.

**The short version:** the model never searches. Your system finds the few pieces of knowledge that matter at question time and hands them over. This is called *grounding*, and retrieval quality decides answer quality.
{: .notice--info}

---

## The deck

Twenty slides: the problem, six retrieval patterns, how Microsoft 365 Copilot grounds its answers, and a reference architecture. Use the arrows, click, swipe, or press the arrow keys once you have clicked inside it.

<div style="position:relative;width:100%;aspect-ratio:16/9;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.25);background:#15202b;">
  <iframe src="/assets/images/posts/2026/11/knowledge-in-agentic-apps/deck.html" title="Knowledge in Agentic Apps (slide deck)" loading="lazy" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
</div>

[Open the deck in its own tab](/assets/images/posts/2026/11/knowledge-in-agentic-apps/deck.html){: .btn .btn--primary}

---

## The problem: a model knows the world, not your organisation

Think of a brilliant new hire who has read every public book but has not yet been given a login. They can reason about anything you put in front of them, but they cannot answer a question about your business until someone hands them the right file. There are three reasons the model cannot simply know your data:

| Problem | Why |
|---------|-----|
| **Private** | Your contracts, emails and meeting notes were never in its training data. |
| **Stale** | Training stops at a cutoff date. Your data changes every hour. |
| **Too big** | Millions of documents will never fit into a context window at once. |

The fix is the same in every case: find the few pieces that matter when the question is asked and give them to the model. Every technique below is a different answer to one question: how do we get the right slice of knowledge into the model at the right moment?

### Six generations, stacked rather than replaced

| # | Generation | The idea |
|---|------------|----------|
| 01 | Keyword search | Match exact words (BM25). Fast, but misses synonyms. |
| 02 | Vector RAG | Turn text into meaning vectors; paste the closest chunks into the prompt. |
| 03 | Hybrid + rerank | Combine keyword and vector results, then re-score the best. |
| 04 | GraphRAG | Add entities and relationships for multi-hop questions. |
| 05 | Agentic retrieval | The model plans, searches several sources, checks, and retries. |
| 06 | Memory + MCP | Persistent memory, plus standard plugs into any system. |

Newer generations do not replace older ones. Production systems stack 03 to 06: hybrid search underneath, graphs and agentic planning on top, memory around it all.

---

## The core patterns

### 1. Retrieval-augmented generation

RAG runs as two loops. Offline, you build the index once and refresh it often. Online, every question runs a search against that index and the best few chunks go into the prompt.

![Retrieval-augmented generation in two loops: offline, documents are parsed and chunked, embedded, and stored in an index; online, a user's question is searched against that index, the top chunks go to the model with the prompt, and it returns an answer with citations](/assets/images/posts/2026/11/knowledge-in-agentic-apps/rag-two-loops.svg)

The key insight is in the middle of the online loop: **the model never searches.** Your code retrieves; the model only reads what it is handed. Bad retrieval means bad answers, however good the model.

Chunking matters more than it looks. Split on headings and sections so each chunk carries a complete thought, and keep the document title and metadata attached to it.

### Embeddings: meaning becomes coordinates

An embedding model turns each chunk into a long list of numbers, and similar meanings land close together. "How many days off do I get?" lands beside the leave-policy chunks without sharing a single keyword with them. Vector search simply finds the nearest neighbours to the question. (Real embeddings have hundreds or thousands of dimensions; the two-dimensional picture in the deck is a simplification.)

### 2. Hybrid search: two searches, one ranked shortlist

Vector search is good at paraphrase and poor at exact strings. Ask for invoice `INV-2231` and the nearest meaning may be a different invoice. So the default is to run both:

- **Keyword (BM25)** catches exact words, codes and names.
- **Vector** catches meaning and paraphrase: "money we owe the supplier".
- **Fusion** (typically Reciprocal Rank Fusion) merges the two ranked lists.
- **A reranker**, a second model, re-reads each shortlisted chunk against the question and re-scores it.

Only the top few go to the model: a small, highly relevant context. This combination is what the mainstream search engines and most vector databases now offer out of the box.

### 3. Knowledge graphs: relationships answer what similarity can't

"Which supplier contracts affect projects Priya leads?" is not a similarity question. No single chunk contains the answer; it sits in the links between a person, a project, a contract and a supplier. Vector search finds look-alike text. A graph follows the links, hop by hop.

- A **knowledge graph** stores entities and relationships explicitly and is queried by traversal.
- **GraphRAG** has a model extract the graph from documents, then summarises clusters of related entities so it can answer "big picture" questions such as which themes recur across every customer call.

### 4. Agentic retrieval: retrieval becomes a reasoning loop

Single-shot RAG struggles when a question is ambiguous, multi-step, or spans several systems. Agentic retrieval hands the search strategy to the model:

1. **Plan**: split the question and choose sources.
2. **Search**: run the sub-queries in parallel.
3. **Reflect**: is there enough good evidence? If not, loop back.
4. **Synthesise**: merge, rank and answer with citations.

Take "Compare our UK and India leave policies and flag what changed this year." The plan produces two sub-queries, both run at once, reflection notices the India result is an old draft and searches again, and the answer comes back side by side with every claim cited. This is the same split I described in [the orchestration patterns post](/concepts/ai/architecture/agentic-orchestration-patterns/): plain RAG is a workflow, where code decides the steps; agentic retrieval is an agent, where the model does.

### 5. Memory: four timescales

| Layer | What it holds | Lasts |
|-------|---------------|-------|
| **Working memory** | The context window: this prompt, retrieved chunks, tool results | One model call |
| **Session memory** | The conversation so far, summarised when it grows long | One chat |
| **Long-term memory** | Facts and preferences the agent saves about a user | Across chats |
| **Organisational knowledge** | Indexes, graphs and systems of record, shared and governed | Permanent |

The top layer is tiny and expensive; the bottom is huge and cheap. Good agents move only what is needed upward, just in time.

### 6. Tools and MCP: one standard plug

Without a standard, every agent needs custom glue for every system, so integrations multiply as agents times systems. The [Model Context Protocol](https://modelcontextprotocol.io/) gives each system one server that any compliant agent can use. A whole retrieval pipeline can then appear to an agent as a single tool. I compared MCP with agent skills in [an earlier post in this series](/concepts/fundamentals/ai/ml/agentic-connectivity-mcp-vs-agent-skills/).

---

## Choosing between them

| Approach | Best for | Weak at | Cost |
|----------|----------|---------|------|
| **Vector RAG** | Fuzzy "what does our policy say about…" questions | Exact codes, names and numbers | Low |
| **Hybrid + rerank** | Most enterprise search: the sensible default | Questions spanning many documents | Low to medium |
| **GraphRAG** | Multi-hop links and themes across a whole corpus | Fast-changing data; keeping the graph current | High to build |
| **Agentic retrieval** | Complex, multi-part questions across sources | Latency and token cost per question | Medium to high per query |

Or, starting from the question:

| If the question sounds like… | Reach for |
|------------------------------|-----------|
| "What does the travel policy say about hotels?" | Hybrid RAG |
| "Find invoice INV-2231" | Keyword (inside hybrid) |
| "Which suppliers link to projects Priya leads?" | Knowledge graph |
| "What themes recur across all customer calls?" | GraphRAG summaries |
| "Compare UK and India policies, then draft an update" | Agentic retrieval |
| "Remember I prefer answers as tables" | Long-term memory |
| "It all lives in Microsoft 365" | Copilot or Copilot Studio first |

---

## The same patterns at the scale of an organisation

Microsoft 365 Copilot is a useful worked example because it runs every pattern above over every email, chat, file and meeting a user can access, grounded per person and per prompt.

### Five steps from prompt to grounded answer

1. **Prompt**: you ask in Word, Teams, Outlook or Copilot Chat.
2. **Ground**: Copilot pulls context from Microsoft Graph and the semantic index, limited to what you can access.
3. **Generate**: the enriched prompt goes to the model.
4. **Check**: after generation, Graph and the index are consulted again, and safety and compliance filters run.
5. **Respond**: the answer, citations and any app commands go back to your app.

Microsoft calls this grounding rather than RAG, but step 2 is retrieval-augmented generation. The difference is that the index, permissions and security are run for you.

### Four building blocks

| Block | What it does |
|-------|--------------|
| **Semantic index** | A vectorised index of Microsoft Graph content. Meaning-based retrieval returns a bounded set of candidates instead of scanning everything. |
| **Microsoft Graph** | The relationship layer: emails, files, meetings, calendar, teams, and who you work with. It is itself a knowledge graph, which is why "who worked with me on X" questions work. |
| **Copilot connectors** | Bring content from non-Microsoft systems into the tenant. |
| **Security trimming** | Indexed data keeps its permissions, sensitivity labels and tenant boundaries. If you cannot find it in Search, Copilot cannot use it. |

The flip side of security trimming deserves a moment: oversharing in SharePoint becomes over-surfacing in Copilot. Search governance is Copilot governance.

### The IQ layers

Microsoft now packages its knowledge layers under an "IQ" name, each grounding a different kind of agent:

- **Work IQ**: the intelligence behind Microsoft 365 Copilot and its agents: organisational data, context and work patterns.
- **Fabric IQ**: business meaning over structured data in Microsoft Fabric and Power BI, so agents understand metrics, not just tables.
- **Foundry IQ**: knowledge bases on Azure AI Search with agentic retrieval. One knowledge base can serve many agents, including over MCP.

The rule of thumb: everyday Microsoft 365 work runs on Copilot and Work IQ; a custom agent over your own sources builds on Foundry IQ.

---

## The reference architecture

Strip away the vendor names and the knowledge stack has five layers. The right-hand column shows where Microsoft's stack does each step for you.

| Layer | What happens | In Microsoft's stack |
|-------|--------------|----------------------|
| **Sources** | SharePoint and files, email and chat, CRM, ERP, tickets, databases and APIs | Copilot connectors |
| **Ingest** | Parse and OCR, chunk by structure, enrich metadata, embed | Semantic indexing |
| **Store** | Vector index, keyword index, knowledge graph, memory store | Semantic index and Graph |
| **Retrieve** | Hybrid search, reranker, graph traversal, agentic planner | Work IQ, Foundry IQ |
| **Reason and act** | Model and prompt, tools via MCP, citations, guardrails | Copilot, Copilot Studio |

Across every layer: identity and permission trimming, evaluation (recall and groundedness), observability, and data governance.

### Six habits of production-grade apps

1. **Trim by permission at query time.** Filter results by the user's identity before the model sees them.
2. **Chunk with structure.** Split on headings and sections; keep titles and metadata with each chunk.
3. **Default to hybrid plus rerank.** Add graphs or agentic loops only when the questions demand it.
4. **Always cite sources.** Citations let users verify answers and expose bad retrieval quickly.
5. **Evaluate continuously.** Keep test sets that score retrieval recall, groundedness and answer quality.
6. **Fix data hygiene first.** Oversharing and stale content become wrong answers. Clean before you index.

---

## Does the deck still hold?

I made the deck in September 2026, so before publishing I checked it against current documentation and coverage.

**The patterns hold.** Hybrid search with reranking is still the standard production baseline, GraphRAG is still described as a targeted upgrade for global, "summarise the themes" questions rather than a starting point, and agentic retrieval is still positioned for complex multi-step questions at a higher cost per query.

**Agentic retrieval is now a dial, not a switch.** In Azure AI Search, "retrieval reasoning effort" has three levels. *Minimal* skips model-based query planning and runs direct text and vector searches; *low*, the default, does one pass of planning and source selection; *medium* adds a second iteration when the first results are not relevant enough. That is the plan, search, reflect loop above, exposed as a cost and latency setting. Parts of it are still in preview.

**Two Microsoft details have moved on since the deck:**

- **Connectors no longer always copy data in.** Alongside the synced connectors that index content into Microsoft Graph, there are now *federated* connectors that query content in place over MCP without indexing it. So "connectors bring content into the tenant" is true of one kind, not all.
- **The IQ family has grown and matured.** It was announced at Ignite 2025; by Build 2026 coverage reports the layers reaching general availability, and later coverage describes a fourth layer, Web IQ, for grounding in the public web. The deck shows three. Microsoft's naming in this area moves quickly, so check Microsoft Learn for the current status before relying on any one of them.

**One word the deck does not use: context engineering.** Much of what the memory slide describes, deciding what reaches the context window and when, is now commonly discussed under that name. The idea is the same; the vocabulary has caught up.

---

## Conclusion

An agent is only as good as what it is given to read. The model reasons; your system decides what it gets to reason about.

- **Retrieval quality decides answer quality.** The model never searches; your code does.
- **Hybrid search with reranking is the default.** Graphs and agentic loops are upgrades for harder questions, and they cost more.
- **Memory is layered.** Move only what is needed into the context window, just in time.
- **Inside Microsoft 365, Copilot runs this stack for you.** Your job is clean, well-permissioned data, because whatever users can find, Copilot can find too.
