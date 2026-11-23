# The Navex delivery harness

This is the contents of `.harness`, the folder the harness installs into a
repository. It is portable: everything the harness needs is in here, and
nothing outside it is modified except the files `harness init` reports before
it writes them.

## What is in this zip

| Path | What it is |
| --- | --- |
| `bin/harness` or `bin/harness.exe` | The harness itself. One binary, no runtime to install. |
| `skills` | Skills authored for this platform, installed beside the vendored ones. |
| `playbooks` | Operator documents the exit codes point at. `playbooks/triage.md` is what exit 1 sends you to. |
| `config.toml` | The configuration template. `init` copies and prefills it. |
| `CONTEXT.md` | What `init` writes into `.harness/context`, and why. |
| `README.md` | This file. |
| `MANIFEST.toml` | A sha256 for every file above. |

`MANIFEST.toml` is not documentation. `bootstrap` verifies every file against
it before anything is unpacked, and `harness self-check` verifies it again at
runtime. A file that is not in the manifest, or does not match it, is a failed
install rather than a warning.

## What does not work yet

One thing in here is not finished, and it fails by telling you so rather
than by behaving oddly.

**`harness eval` has no cases to run.** The runner is in the binary and the
format is documented, but no eval suite ships yet, so a run reports nothing to
do.

## Installing

The supported route is the bootstrap script, which `harness init` writes into
the repository. It fetches the pinned version from the internal feed, verifies
the manifest, and only then moves anything into `.harness/bin`:

    ./bootstrap.sh          on Linux, macOS and WSL
    bootstrap.bat           on Windows

Binaries are never committed. The bootstrap scripts are, and the `.gitignore`
entry that keeps `.harness/bin` out of git is written for you.

To install this zip by hand instead, unpack it over `.harness` in the target
repository, replacing what is there, and then run:

    .harness/bin/harness init

## What init writes here

`harness init --install` writes `HARNESS.md` into this folder: the standing
instructions every agent session reads. The repository's own `CLAUDE.md` gains
one line, `@.harness/HARNESS.md`, which loads it, and nothing else in that file
is touched. `harness init --restore` takes the line out again. A tool whose
instruction file cannot load another file carries the same text inline,
between two marked lines, instead.

It also writes `CONSTITUTION.md`: what no run in this repository may do, as
numbered rules a review can cite. The N rules ship with the harness. The P
rules are this project's own, written by its team in `project-constitution.md`
in this folder, one `- ` item per rule, and committed. Edit that file, never
`CONSTITUTION.md`; `harness constitution` prints the current text.

`facts/` is this project's facts, written by its team: modules, workflow,
teams, suites and gates, at a high level. From a checkout, `harness facts
publish` sends the folder to the service. Where there is no checkout, as for an
analyst, `harness facts pull` writes the published set here and `harness facts
show` prints it without writing. A pull never overwrites a file it did not
write.

## After installing

    harness init            install hooks and shims, prefill config.toml
    harness doctor          check the install, the config and what is reachable
    harness config          read and change a setting; --local keeps it personal
    harness self-check      verify every file against MANIFEST.toml

`doctor` is the one to run when something is not behaving. It reports what is
configured, what is reachable, and what is missing, and it distinguishes the
three rather than reporting one failure.

## Configuration

`config.toml` carries settings. It never carries secrets: a secret is written
as an indirection to an environment variable.

    api_key = "env:HARNESS_MMS_API_KEY"

A literal is accepted so a value can be tried quickly, but `doctor` reports it
as a finding. Supply real values through the platform's secret store.

An unset `mms.url` is not a failure. Telemetry spools to disk and is delivered
once a url is configured, so nothing is lost by installing before the service
is reachable.

## Exit codes

The harness treats these as a contract, so a script can branch on them.

| Code | Meaning |
| --- | --- |
| 0 | ok |
| 1 | failure |
| 2 | rejected at a gate |
| 3 | guardrail |
| 4 | missing prerequisite |

## Support

The version this zip was built from is in `MANIFEST.toml`. Quote it when
reporting a problem, along with the output of `harness doctor`.
