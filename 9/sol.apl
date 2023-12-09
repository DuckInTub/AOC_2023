⍝ Solution 2023 day 9
d←⍎¨¨' '(≠⊆⊢)¨⊃⎕NGET 'input.txt' 1
O←,0
+/{O≡∪⍵:⍵ ⋄ (⊃⌽⍵)+⊃∇2-⍨/⍵}¨d ⍝ Part 1
+/{O≡∪⍵:⍵ ⋄ (⊃⍵)-⊃∇2-⍨/⍵}¨d  ⍝ Part 2
