" Vim syntax file
" Language: ob files
" Author: Nithin Nayak Sujir

" Define keywords
syn keyword obPreCondit package
syn keyword obStatement import extends
syn keyword obType uint8 uint16 uint32 float32 string uint64 bool const sint8 sint16 sint32
syn keyword obConditional hideable customSet mgmtMandatory customMgmtAdd
syn keyword obConst true false Locked UnLocked Maintenance Available UnAvailable Enabled Disabled 
syn keyword obFunction group range authority error enum list pName owName
syn keyword obFunction maxLength tl1KeyParm action alarm moName desc
syn keyword obOperator RW RO alt p ow wow

syn region	obComment	start="//" skip="\\$" end="$" keepend

syn match   obNumber	"\<0x\x\+[Ll]\=\>"
syn match   obNumber	"\<\d\+[LljJ]\=\>"
syn match   obNumber	"\.\d\+\([eE][+-]\=\d\+\)\=[jJ]\=\>"
syn match   obNumber	"\<\d\+\.\([eE][+-]\=\d\+\)\=[jJ]\=\>"
syn match   obNumber	"\<\d\+\.\d\+\([eE][+-]\=\d\+\)\=[jJ]\=\>"

syn region obString		matchgroup=Normal start=+[uU]\='+ end=+'+ skip=+\\\\\|\\'+ 
syn region obString		matchgroup=Normal start=+[uU]\="+ end=+"+ skip=+\\\\\|\\"+ 
syn region obString		matchgroup=Normal start=+[uU]\="""+ end=+"""+ 
syn region obString		matchgroup=Normal start=+[uU]\='''+ end=+'''+ 


" Highlight
hi link obPreCondit PreCondit
hi link obStatement Statement
hi link obType Type
hi link obComment Comment
hi link obConst Constant
hi link obNumber Number
hi link obFunction Function
hi link obOperator Operator
hi link obConditional Conditional
hi link obString String

let b:current_syntax = "ob"
