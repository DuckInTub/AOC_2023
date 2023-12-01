⍝ Solution 2023 day 1
score←{+/⍎∘(⊃,⊃∘⌽)¨⍵}
score {⍵/⍨⍵∊⎕D}¨d←⊃⎕NGET 'input.txt' 1

s←'one' 'two' 'three' 'four' 'five' 'six' 'seven' 'eight' 'nine'
ptrn←'\d|',⊃{⍺,'|',⍵}/s
d←{ptrn⎕S'&'⍠'OM'1⊢⍵}¨d
score {10≠r←s⍳⊂⍵:⍕r ⋄ ⍵}¨¨d
