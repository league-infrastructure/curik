---
title: "Post-sequester user choices \u2014 import outline and research alignment"
status: done
sprint: '013'
tickets:
- '001'
---

After sequestering/analyzing old content, the start-curik agent should present
additional choices to the user with structured UI menus before beginning
Phase 1a.

## 1. Import existing outline

Offer to extract the module/lesson structure from the old content and import
it into Curik as the starting course structure outline. Instead of building
from scratch, pre-populate the spec's Course Structure Outline (section 5)
from what was found in `_old/`.

This means the agent would parse the old directory tree, identify
modules/lessons/topics, and present them as a proposed outline the user can
accept, edit, or reject.

## 2. Research alignment

Offer to run Phase 1c research immediately after the content analysis,
comparing the old curriculum's topics against external standards,
certifications, and similar courses. Frame it as: "Let's see how your
existing course aligns with what's out there."

This gives the user context about whether their existing content maps to a
known standard (PCEP, AP CS, etc.) before they commit to a direction in
Phase 1a. If it does, the user may want to formalize that alignment. If it
doesn't, they know they're building something custom.

## Where this fits

These should appear as numbered menu options in the start-curik agent flow,
after the content analysis panel is shown and before Phase 1a begins.
Something like:

```
### What would you like to do next?

1. **Import the existing outline** — I'll extract the structure from your
   old content and use it as a starting point
2. **Research alignment** — Let's see how your existing topics compare to
   standards and certifications before we start designing
3. **Start fresh** — Jump straight into the course concept conversation
```
