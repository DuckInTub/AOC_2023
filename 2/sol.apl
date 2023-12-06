⍝ Solution 2023 day 2

⍝ Regex out strings of "{number} {r|g|b}
⍝ Note: You can comfortably parse this without regex.
d←('\d+ \w'⎕S'&')¨⊃⎕NGET 'input.txt' 1

⍝ For each _ in ⍺ group ⍵ by if it contains _
group←{/∘⍵¨↓⍺∘.∊⍵}
⍝ Extract the numbers into buckets for _ in ⍺
bucket←{{⍎¯2↓⍵}¨¨⍺ group ⍵}

mx←{⌈/¨'rgb'bucket ⍵}¨d
+/⍸{~∨/12 13 14<⍵}¨mx ⍝ Part 1
+/×/¨mx ⍝ Part 2