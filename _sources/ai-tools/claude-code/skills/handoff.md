---
description: Draft a handoff with where we stopped and final decisions, then ask where to save it
---

Prepare a handoff document so a new session can continue exactly where we stopped without any chat history. It must contain only what is final and settled.

STRICT RULES:
- Include only final decisions, completed work, the current state, and where we stopped.
- Do NOT include discussions, debates, brainstorming, options we considered, or how we reached a decision.
- If a decision changed during the conversation, record only the latest version.
- If something was discussed but not decided, do not record it as a decision. List it under "Undecided" in one line.
- Write each item as a short, direct statement. No narrative.
- Reference file paths and function names instead of pasting code.

Sections:

1. **Where we stopped**: the exact point the work paused. Include:
   - The task in progress right now.
   - The last thing completed, and the file or change it touched.
   - Anything half-done (for example, a function partly written or a test still failing), and what remains to finish it.
   - The single immediate next action to take.
2. **Project**: goal, stack, structure (brief).
3. **Decisions**: one line each, as a final statement. Example: "Use PostgreSQL for storage."
4. **Do not use**: approaches that were ruled out, one line each with a short reason, so they are not retried. Example: "No Redis caching: adds deployment complexity."
5. **Completed**: what is done, with the files changed.
6. **Current state**: what works, what is broken.
7. **Next steps**: concrete, ordered actions after the immediate next action.
8. **Undecided**: open questions only, one line each, no discussion.
9. **Verify**: exact commands to run, build, and test, with expected results.
10. **Key files**: important files and their purpose.

$ARGUMENTS

SAVING:
- Do not write any file yet. First draft the full content.
- Then ask me: "Where should I save the handoff? Give a full path, or the path of an existing handoff to update."
- If I give an existing handoff file, read it first and update it: replace anything outdated or superseded, and do not keep old versions or history.
- If I give a new path, create the file there.
- After saving, show the full path, give a 3-line summary of what changed, and remind me to run /clear and then /pickup <path>.