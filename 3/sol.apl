⍝ Solution 2023 day 3
d←↑⊃⎕NGET 'input.txt' 1
nums←⍎¨⊃,/{⍵⊆⍨⎕D∊⍨⍵}¨↓d
sp←∪(⎕D,'. ')~⍨,d
id←(⍴d)⍴(⎕D∊⍨,d)×+\∊{2</0,⎕D∊⍨⍵}¨↓d
+/nums⌷⍨⊂0~⍨∪,id×{∨/sp∊⍵}⌺3 3⊢d

+/{×/nums[⍵]}¨0~⍨,{(2=≢i←¯1 0~⍨,⍵)∧¯1=⍵[2;2]:⊂i ⋄ 0}⌺3 3⊢id-'*'=d

