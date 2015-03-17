" Vim syntax file
" Language: sloginfo output
" Author: Nithin Nayak Sujir

syn match	slogDate	/^.\{-}\d\d:\d\d:\d\d/	
syn match slogDate /\d\d\d\d.\d\d.\d\d \d\d:\d\d:\d\d/
syn match slogDate /\d\d:\d\d:\d\d/
syn match	slogProcName	/\a\(\a\|\d\)\+:\(\a\|\d\)\+/
syn match slogClassFunction /\a*\d*::\a*\d*/

syn region slogKilling start="Killing" end="$" keepend
syn region slogKilling start="signal.*caught by process" end="$"
syn region slogKilling start="Assertion failure" end="$"
syn match slogFileName /\a\(\a\|\d\)*\.cpp:\d*/
syn match slogNv /\(\a\|\d\)\+ N=/
syn match slogNv /\/\(B\|U\d\{1,2}\|S\d\{,2}\)/
syn region slogString start="\"" end="\""

syn region slogSpawn start="Spawning child" end="$"

hi link slogDate 	Comment
hi link slogKilling PreCondit
hi link slogFileName Number
hi link slogProcName Statement
hi link slogClassFunction Function
hi link slogType Type
hi link slogNv Function
hi link slogString    String
hi link slogSpawn Statement


let b:current_syntax="slog"
