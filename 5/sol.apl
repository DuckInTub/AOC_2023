⍝ Solution 2023 day 5

p←⍎¨¨{⍵⊆⍨∨/¨∊∘⎕D¨⍵}{⍵/⍨⍵∊⎕D,' '}¨⊃⎕NGET 'test.txt' 1
seed←,⊃↑¨p
maps←1↓p

amap←{1=≢n←0~⍨⍵{os is r←⍺ ⋄ (⍵<is+r)∧is≤⍵:os+⍵-is ⋄ 0}⍨¨⍺:⊃n ⋄ ⍵}
⌊/⊃{⍺∘amap¨⍵}/(⊂seed),⍨⌽maps

seed←↑{⍺,⍺+⍵}/{(2÷⍨≢⍵)2⍴⍵}seed

⍝ Reverse search
rmaps←⌽{os is r←⍵ ⋄ is os r}¨¨maps
⌊/⊃{⍺∘amap¨⍵}/(⊂seed),⍨⌽maps

in_range←{rs re←⍵ ⋄ (⍺≥rs)∧⍺<re}


⍝ Implement map for a range
rmap←{
    ⍝ Ranges are [s, e) ; s,e ∊ N
⍝     [ss              se]
⍝                              [rs       re]

    os is r←⍺
    rs re←is,is+r
    ss se←⍵
    ~(rs<se)∧re>ss:0
    ⎕←'Overlapped'
    ovlp←(ss⌈rs),se⌊re

    after←(se⌊re),se
    before←ss,ss⌈rs
    ov←os+ovlp-is
    ret←after ov before
    ret/⍨≠/¨ret
}

⊃{∪⊃,/,⍺ ∘.rmap ⍵}/⌽maps,⍨⊂↓seed
