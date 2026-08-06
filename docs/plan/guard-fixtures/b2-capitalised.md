DELIBERATELY VIOLATING — B2. RETIRED_PHRASES had no re.IGNORECASE while
SIZING_PHRASES did.

The capital must be LOAD-BEARING. The first version read "The ten local
terms", and `ten local terms` matches lowercase inside it, so the fixture
passed with IGNORECASE deleted — it tested nothing. Measured, then fixed.

Ten local terms are declared at P5.
