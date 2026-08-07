# DELIBERATELY CLEAN — the OVER-EXCLUDE direction, which is the point

The same phrase as `live-reintroduction.md`:

this exact string was retracted and must not return

This file sits inside `scripts/sweep-fixtures/`, an excluded path, so the
sweep must NOT report it.

WHY THIS FIXTURE EXISTS. Two failure directions and they are not
symmetric. Forgetting an exclusion reports history as live — noisy, and
the first run corrects it. Over-excluding reports LIVE TEXT AS HISTORY,
silently, and a live claim written into an excluded path is invisible to
the instrument.

No match-direction fixture can demonstrate that. This one asserts the
exclusion behaves as declared, which is the direction this project had
never exercised when the sweep was built.