# docs/

| Path | Holds | Writer |
|---|---|---|
| `measure/` | measure-stage documents — blast radius, surface, bindings, fixtures, cost | H |
| `plan/` | plan-stage documents — items, dependencies, topological order | H |
| `measure/part1-carried-findings.md` | findings produced in one unit that belong to a later one — recorded, never decided there | H |
| `experiments/` | experiment records — setup, prediction stated in advance, result, falsifier | H |
| `coverage.md` | the capability matrix | H |
| `sources/` | the authoritative source register | human |
| `reference/` | external specifications cited by ADRs | human |
| `prompts/` | session prompts | human |

**Gate content lives here; `review-inbox.md` is the channel.** A
`[H → O]` message names the document, states its assertions and
falsifiers in summary, and requests falsification. The document carries
the work. This keeps the inbox reviewable and puts the substance under
version control.

**`review-inbox.md` and `review-inbox-archive/` are tracked, and this
paragraph used to say they were gitignored.** Corrected 2026-08-05.
Nothing ignored them — `git check-ignore -v review-inbox.md` matches no
rule, `.git/info/exclude` is empty and there is no
`core.excludesfile`. **They had simply never been added**, and
`git status --short` had been printing `?? review-inbox.md` on every run.
A claim about repository state, written into a document, checkable by one
command, never checked — while the answer was in the output of a command
run dozens of times.

The consequence was not cosmetic: **O could not dispose two proposed
claims**, because §1 forbids reconstructing wording it cannot read, and
the proposals existed only in a working tree it has no access to.

Design-stage decisions go to `design/ADR-*`, not to a `docs/design/`
directory. One ADR per structural decision, numbered, dated, never
edited after acceptance — supersede instead.

Documents are amended in place, with amendment history visible at the
top. Corrections stay recorded rather than being edited away.
