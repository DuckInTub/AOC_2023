⍝ Solution 2023 day 7

⍝ (h)ands & (b)ids
h←⊣/p←↑' '(≠⊆⊢)¨⊃⎕nget 'input.txt' 1
b←⍎¨⊢/p

⍝ Get type of hand
t←(5 0)(4 1)(3 2)(3 1)(2 2)(2 1)(1 1)
type←{t⍳⊂2↑(⊂∘⍒⌷⊢){≢⍵}⌸⍵}
⍝ Card values
v←⌽⎕D,'TJQKA'
+/b×⍋⍒↑(type,v∘⍳)¨h ⍝ Part 1

⍝ Get type of hand with jokers
typeJ←{jc←+/'J'=⍵ ⋄ t⍳⊂(jc 0)+2↑(⊂∘⍒⌷⊢){≢⍵}⌸⍵~'J'}
⍝ Card values
v←'J',⍨⌽⎕D,'TQKA'
+/b×⍋⍒↑(typeJ,v∘⍳)¨h ⍝ Part 2
