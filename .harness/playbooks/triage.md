# Triage: the harness exited 1

This is the document the exit code contract points at. A command exited 1 and
you want to know what to do about it.

Read the first section to find out whether you are in the right document. Then
work the checks in order and stop at the first one that explains the failure.
The order is not arbitrary: each check rules out a class of cause, and running
them out of order produces answers that look like findings and are not.

## What the code means

Exit 1 is **failure**: the command tried to do what was asked and could not.
That is a narrow claim, and the other four codes are what make it narrow.

| code | meaning | this document applies |
| --- | --- | --- |
| 0 | the command did what was asked | no |
| 1 | the command failed | yes |
| 2 | a human rejected the action at a gate | no |
| 3 | a guardrail refused the action | no |
| 4 | something the command depends on is absent | no |

Three of those are routinely mistaken for exit 1, and each has its own answer:

- **Exit 2** is a person saying no at a HITL gate. The system worked. Do not
  retry, do not rerun with different arguments, and do not look for a fault.
  The next step is a conversation, not a command.
- **Exit 3** is a guardrail: most often a write attempted without
  `--confirmed`. The fix is to take the action to a gate and get an accept,
  never to add the flag because the command asked for it.
- **Exit 4** is a missing prerequisite: a binary, a config value, a token, a
  vendored tree. It is separate from 1 precisely so that a caller can offer to
  install or configure rather than retry. If you got 4, install or configure
  the thing the message named and run the command again.

If the code was 2, 3 or 4, stop here. Nothing below applies.

## Check in this order

Run each check, read its output, and stop at the first one that explains what
you saw. Every step below is read only.

### 1. Read the error line

The harness prints one line to stderr on a failure, in the form
`error: <what went wrong>`. It names the thing that failed and, where there is
one, the path involved.

Do this before anything else. Most exit 1 failures are fully explained by their
own message, and the remaining steps exist for the ones that are not.

### 2. `harness doctor`

    harness doctor

Eight checks, one row each, `ok` or `fail` with a detail column. A failing row
here explains most failures that the error line did not.

| row | fails when |
| --- | --- |
| `binaries` | `.harness/bin` has no harness binary. Run the bootstrap script. |
| `hashes` | there is no `MANIFEST.toml`, or a file no longer matches it |
| `config` | `.harness/config.toml` is absent or does not parse |
| `tokens` | a credential the configuration names is not in the environment |
| `mms` | the measurement service is not configured or not reachable |
| `hooks` | the settings entry, the telemetry shims or the git hooks are missing |
| `adapter` | the configured tool host or AI client could not be selected |
| `index` | the context files have not been generated |

`doctor` exits 0 even when rows fail. It reports; it does not decide. A row
that fails is a finding, not a verdict on the command you were running.

Two rows deserve care because they look like faults and often are not:

- `tokens` fails on a credential that is simply not needed by the command you
  ran. A repository that never reads Jira fails the Jira token row forever.
- `mms` fails when telemetry is spooling to disk rather than being delivered.
  Nothing is lost while it spools. See step 5.

### 3. `harness self-check`

    harness self-check

Re-hashes every installed file against `MANIFEST.toml`. Use it when `doctor`
reported `hashes` as failing, or when a command failed in a way the message
could not account for.

A mismatch here means an installed file is not the file that was shipped. Do
not edit it back. Reinstall from the dist with `harness self-update`, then run
the original command again.

### 4. The vendored tree

    harness skills sync-upstream

Only if the failure involved skills, commands or the configuration layer. The
vendored upstream tree is verified against its `.sha256` manifest, and drift is
a hard stop rather than a warning: every drifted file is reported in one pass.

Drift means somebody edited a tree that is meant to be verbatim. Restore the
file from upstream or re-vendor and regenerate the manifest. Do not regenerate
the manifest alone. That makes the check agree with the edit and removes the
only thing that would have caught the next one.

### 5. The telemetry spool

    harness telemetry flush

Only if the failure was in delivering telemetry. Records spool to
`.harness/scratchpad/telemetry-spool.jsonl` when the service is unreachable and
drain when it comes back, so an unreachable service is not a lost record and is
not a reason to stop working.

A spool that never drains is a configuration problem, not a delivery problem:
go back to the `mms` row in step 2.

## When to stop

Stop and hand it on when any of these is true. Each one means the next useful
step is somebody else's, and continuing produces noise rather than an answer.

- **The error line names something outside this repository.** A service that
  is down, a credential that was revoked, a network that refuses. Nothing in
  the harness will fix it and rerunning will not diagnose it.
- **`doctor` is all `ok` and the command still fails.** The failure is not in
  the installation. Capture the exact command, its full output and the harness
  version from `harness version`, and raise it. Do not start changing
  configuration to see what happens.
- **A check contradicts the error line.** Two sources disagreeing is worth
  reporting as it stands. Resolving it by picking the one you prefer is how a
  real fault gets closed as a configuration mistake.
- **The fix would edit a generated or vendored file.** Anything under
  `.harness/upstream`, anything between the harness managed markers, and
  anything `MANIFEST.toml` pins. The edit will be overwritten or will fail the
  next verification, and it will look like a fresh fault to whoever meets it.
- **You have run the same command three times.** A command that fails
  identically three times is not intermittent. Move to the checks, or stop.

## What not to do

- Do not pass `--confirmed` to get past a refusal. That flag says a human
  accepted at a gate. Passing it because a command asked for it makes the
  intervention log say something that did not happen.
- Do not delete `.harness` and reinstall as a first move. It discards the
  spool, the intervention log and the resume state, which are the three things
  that would have told you what happened.
- Do not edit the vendored tree to make a check pass.
