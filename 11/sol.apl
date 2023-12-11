⍝ Solution 2023 day 11
g←⍸'#'=m←↑d←⊃⎕NGET 'input.txt' 1
er←⍸~'#'∊¨d
ec←⍸~'#'∊¨↓⍉m
f←-⍥⊃
dist←f+⍥|f⍥⌽

gdist←{
     r1 c1 r2 c2←⍵
     expF←⍺-1
     in←{l h←⍵ ⋄ (l≤⍺)∧⍺≤h}
     f←⌊,⌈
     g←+⍥(+/)
     vr←r1 f r2
     hr←c1 f c2
     nr←≢er/⍨in∘vr¨er
     nc←≢ec/⍨in∘hr¨ec
     ((r1 c1)dist(r2 c2))+expF×nr+nc
 }

t←t←0⍪⍨0,⍉↑⍴∘1¨⍳¯1+≢g
+/2∘gdist¨g_c←t/⍥,∘.,⍨g

⎕PP←32
+/1E6∘gdist¨g_c
