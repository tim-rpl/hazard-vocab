# Fixtures

Real captured payloads, unmodified, with capture timestamp and source
URL recorded alongside.

Used for:

- SHACL validation (`make check`)
- the T1 confluence test — replay in N shuffled orders, diff outputs
- the C3 arity test — canonicalize, plot arity distribution and count
  distinct role sets

Do not hand-write fixtures. Synthetic data will validate against a
schema that real data breaks. Capture, don't invent.

## The verification-tier constraint

"Capture, don't invent" is the rule, but it is not always satisfiable,
and the failure is not uniform across sources. Per
`docs/sources/HDC-data-source-register.html`, each source carries a
verification tier:

| Tier | What can be captured |
|---|---|
| `Confirmed live` | A real payload. Capture it. |
| `Documented` | Endpoint and schema are confirmed against the publisher's documentation, but the source has not been watched working end to end. A capture may still succeed — attempt it, and record which. |
| `Unverified` | Neither. There may be no capturable payload at all. |

Three sources are `Unverified` (GDELT, USA Structures, the wildfire
camera layer) and several are `Documented`. The register also records
that the reference implementation's development environment blocks
outbound access to every live data host — which is why those tiers
exist at all.

Two consequences for this repository:

1. **The tier is a property of the fixture, so record it.** Alongside
   capture timestamp and source URL, record the register tier at time
   of capture and whether the payload was observed or reconstructed
   from documentation. A fixture derived from a schema document is not
   a captured payload and must not be filed as one — it is the exact
   thing "capture, don't invent" forbids, and it is invisible after the
   fact unless labelled.
2. **A source with no capturable payload is a fixture gap, not a
   licence to synthesise.** Record the absence. A part validated only
   against sources that happened to be reachable has a coverage
   boundary, and that boundary should be legible from this directory
   rather than inferred from what is missing.

The register's environment constraint describes the reference
implementation's environment, not necessarily this one. Probe before
assuming; a source marked `Documented` there may be capturable here,
and the tier should then be recorded as observed-here rather than
silently upgraded in the register, which is a human-owned file.
