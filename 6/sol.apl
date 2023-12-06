⍝ Solution 2023 day 6
PQ←{P←(-⍺)÷2 ⋄ D←(⍵-⍨P*2)*0.5 ⋄ P∘(-,+)D}
races←{1+{(⌈⍵)-⌊⍺}/1 ¯1+(-⍺) PQ ⍵}
⍝ Part 1
×/races⌿↑{⍎¨⍵⊆⍨⎕D∊⍨⍵}¨d←⊃⎕NGET 'input.txt' 1
⍝ Part 2
races/{⍎⍵/⍨⎕D∊⍨⍵}¨d
