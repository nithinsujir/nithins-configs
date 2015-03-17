" Vim color file
" Maintainer: iyerns <iyerns AT gmail DOT com>
" 
" Comments are welcome !
" Spammers will be shot. Survivors will be shot again
" 
" Last Change: 25 August 2005
" Version:1.2
" Changes:Supports professional colors for file browsing
" Comment: Atlast, a professional colorscheme for Vim
" Released by popular demand. in case other highlighting 
" terms are to be included, please feel free to add those 
" and send me your updated .vim file :) to be included in 
" the next version.If there are enough requests, I will 
" release a cterm version also. 
"
" Uses only safe HTML colors
"

set background=light
hi clear
if exists("syntax_on")
	syntax reset
endif
let g:colors_name="professional"

hi Normal   guifg=black	 guibg=#ffffcc 
hi Statusline    gui=none guibg=#006666 guifg=#ffffff
hi  VertSplit    gui=none guibg=#006666 guifg=#ffffff
hi StatuslineNC  gui=none guibg=#666633 guifg=#ffffff

hi Title    guifg=black	 guibg=white gui=BOLD
hi lCursor  guibg=Cyan   guifg=NONE
hi LineNr   guifg=white guibg=#006666 
"guibg=#8c9bfa

" syntax highlighting groups
hi Comment    gui=NONE guifg=grey52
hi Operator   guifg=#ff0000

hi Identifier guifg=#339900 gui=NONE

hi Statement	 guifg=chocolate1 gui=NONE
hi TypeDef       guifg=#c000c8 gui=NONE
hi Type          guifg=royalblue1 gui=NONE
hi Boolean       guifg=#0000aa gui=NONE

hi String        guifg=indianred1 gui=NONE
hi Number        guifg=#9933ff gui=NONE
hi Constant      guifg=#ff8080 gui=NONE

hi Function      gui=NONE      guifg=#6600ff 
hi PreProc       guifg=purple3 gui=NONE
hi Define        gui=bold guifg=#ff0000 

hi Keyword       guifg=#ff8088 gui=NONE
hi Search        gui=NONE guibg=#ffff00 
"guibg=#339900
hi IncSearch     gui=NONE guifg=#ffff00 guibg=#990000
hi Conditional   gui=none guifg=cyan4
hi browseDirectory  gui=none guifg=#660000 guibg=#ffffff

