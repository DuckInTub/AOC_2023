⍝ Solution 2023 day 4
d←⍎¨¨'|'∘(≠⊆⊢)¨{1↓⍵/⍨∨\':'=⍵}¨⊃⎕NGET 'input.txt' 1
+/⌊2*¯1+c←≢¨↑∩/¨d

⍝ What other cards does each card win:
⍝ in the form of a matrix such that r→c
m←↑c{(⍺/0),⍵/1}⍨¨⍳≢c
id←∘.=⍨⍳

⍝ Converges to this
⍝ {1+⍵+.×m}⍣≡⊢1 → ⌹m-⍨id≢c
⍝ https://mast.queensu.ca/~math211/m211oh/m211oh96.pdf
+/∊⌹m-⍨id≢c
