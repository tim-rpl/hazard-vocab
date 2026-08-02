-- DELIBERATELY CLEAN. A comment that writes out the forbidden pattern
-- while containing no vacuous theorem. The grep rule fired on exactly
-- this shape. See [H -> O] plan gate block response 2, BR-7.
/- An artifact can fail by concluding `True` — that is, by a statement
   of the form `theorem foo : True := by trivial` — or by carrying a
   `sorry` that can never close, or by proving a hypothesis from
   itself. -/
theorem real_statement (n : Nat) : n + 0 = n := by simp
