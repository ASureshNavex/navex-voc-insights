# Repository context

`harness init` reads the repository and writes what it found into
`.harness/context`. This file explains what is in there, because the files
themselves are generated and a reader who has not seen this will reasonably
assume somebody wrote them by hand.

## What is generated

`init` scans the repository once and records what it can establish without
guessing: the projects and their languages, the entry points, the test layout,
the dependency edges between projects, and the shape of the build. `doctor`
reads the architecture file back and reports when it is missing or stale.

Nothing in `.harness/context` is authored. Editing a file there is safe but
pointless: the next `init` overwrites it.

## Why it is on disk rather than computed each time

Two reasons, and both matter more than the disk it costs.

A scan walks the whole repository. Doing that on every command would make the
fast commands slow, and the commands that use context are the ones a developer
runs most.

More importantly, it makes the context reviewable. What the harness believes
about a repository is a file somebody can open and disagree with, rather than
something that only exists inside a model's prompt. When a skill produces a
wrong answer, the first question is what it was told, and this is the answer.

## Keeping it current

    harness init            rescan and rewrite
    harness doctor          report whether it is present and readable

Re-run `init` after a change that moves projects around, adds a language, or
changes how the repository builds. A stale context is not corrupt, it is out of
date, and `doctor` says which.

## What is not here

Secrets are not here, and neither is source code. The context files describe
structure: names, paths, languages, relationships. If something in here looks
like a credential, that is a defect worth reporting rather than a value worth
using.
