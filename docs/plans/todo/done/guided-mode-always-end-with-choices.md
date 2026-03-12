---
status: done
sprint: '013'
tickets:
- '002'
---

# Guided mode — every stop should end with choices

The curriculum developer using Curik likely doesn't know the process. They
don't have strong opinions about what comes next. The system should lead them.

## Core idea

At the start of the session, ask the user whether they want a **fully guided
experience**. If they do (and most will), then every time the agent stops
talking during Phase 1, it should end with:

1. A question about what the user wants to do
2. Numbered options they can pick from

Never leave the user staring at a blank prompt wondering "what do I type now?"

## Examples of what this looks like

After capturing the course concept:
```
### What would you like to do?

1. **Looks good — move on** to pedagogical model (Phase 1b)
2. **Change something** — I want to revise part of the concept
3. **Tell me more** — explain what Phase 1b involves before we go there
```

After the agent presents research findings:
```
### What next?

1. **This is enough** — let's move to alignment decisions
2. **Dig deeper** — research more about [specific topic]
3. **I found something** — let me share a resource I know about
4. **Start over** — research in a different direction
```

After presenting the tier determination:
```
### Does Tier 3 sound right?

1. **Yes** — continue with Tier 3
2. **No, I think it should be Tier 2** — explain why
3. **I'm not sure** — explain the difference between tiers
```

## The principle

The user is the educational expert. The agent is the process expert. The agent
should always be driving — presenting what it knows, making recommendations,
and offering clear next steps. The user steers by picking options and
overriding when they disagree.

This is especially important because curriculum developers are not software
people. They won't know to say "advance to phase 1b" or "run research."
The options menu teaches them the process while they use it.
