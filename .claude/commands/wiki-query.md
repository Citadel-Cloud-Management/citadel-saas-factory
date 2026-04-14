---
name: wiki-query
description: Answer a research question against the LLM Wiki. Files valuable answers back as new wiki pages.
argument-hint: <question>
---

# /project:wiki-query

Answer a research question against the compiled LLM Wiki, and file the valuable answer back into the wiki so explorations compound.

**Question:** $ARGUMENTS

## What this does

1. **Reads** `docs/vault/wiki/index.md` first. **The wiki is the first lookup, not raw grep.**
2. **Greps** `docs/vault/wiki/` for the question's key terms to find relevant entity, concept, comparison, and source pages.
3. **Reads** matching pages.
4. **Synthesizes** an answer with citations back to wiki pages.
5. If the wiki is thin on this topic, reads relevant `docs/vault/raw/` sources and **queues an ingest** for anything material.
6. **Offers to file the answer back** as:
   - `wiki/comparisons/<slug>.md` for A-vs-B questions
   - `wiki/concepts/<slug>.md` for definitional questions
   - An update to an existing entity/concept page
7. **Appends** to `docs/vault/wiki/log.md`:
   ```
   ## [YYYY-MM-DD] query — <short>
   ```
   with a pointer to any new page created.

## Instructions for Claude

1. Invoke the `llm-wiki` skill via the Skill tool before touching any files.
2. Always read `wiki/index.md` before grepping raw files — the compiled knowledge is the first lookup.
3. Cite wiki pages in your answer, not raw files.
4. After answering, explicitly ask the user: `File this answer back into the wiki as [[wiki/<category>/<slug>]]? (y/N)`.

## Vault Links

- [[../skills/llm-wiki/SKILL|llm-wiki skill]]
- [[../agents/wiki-curator|wiki-curator agent]]
- [[../../docs/vault/wiki/index|Wiki Index]]
- [[wiki-ingest|/project:wiki-ingest]]
- [[wiki-lint|/project:wiki-lint]]
