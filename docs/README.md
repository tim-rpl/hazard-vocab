# docs/

| Path | Holds | Writer |
|---|---|---|
| `measure/` | measure-stage documents — blast radius, surface, bindings, fixtures, cost | H |
| `plan/` | plan-stage documents — items, dependencies, topological order | H |
| `experiments/` | experiment records — setup, prediction stated in advance, result, falsifier | H |
| `coverage.md` | the capability matrix | H |
| `sources/` | the authoritative source register | human |
| `reference/` | external specifications cited by ADRs | human |
| `prompts/` | session prompts | human |

**Gate content lives here; `review-inbox.md` is the channel.** A
`[H → O]` message names the document, states its assertions and
falsifiers in summary, and requests falsification. The document carries
the work. This keeps the inbox reviewable and puts the substance under
version control — `review-inbox*.md` is gitignored, so anything left
only in the inbox is not in the repository at all.

Design-stage decisions go to `design/ADR-*`, not to a `docs/design/`
directory. One ADR per structural decision, numbered, dated, never
edited after acceptance — supersede instead.

Documents are amended in place, with amendment history visible at the
top. Corrections stay recorded rather than being edited away.
