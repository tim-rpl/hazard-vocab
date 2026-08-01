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
