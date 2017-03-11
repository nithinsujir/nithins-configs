set nocompatible
filetype off

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
Plugin 'L9'
"Plugin 'FuzzyFinder'
Plugin 'will133/vim-dirdiff'
Plugin 'EasyMotion'
Plugin 'QFixToggle'
Plugin 'wincent/command-t'


call vundle#end()            " required
filetype plugin indent on    " required

behave mswin
syntax on

"Abbreviations
abbreviate #d #define
abbreviate #i #include
inoremap #e<space> #endif
inoremap #if<space> #ifdef

"C keywords
abbreviate br break
abbreviate ca case
abbreviate ccout cout << "-----------[ " << __FUNCTION__ << "@" << __FILE__ << ":" << __LINE__ << " ]--------------------------------" << endl
abbreviate co continue
abbreviate de default
abbreviate el else
abbreviate ex extern
abbreviate i8 int8
abbreviate i1 int16
abbreviate i3 int32
abbreviate inl inline
abbreviate lo long
abbreviate ret return
abbreviate reg register
abbreviate si sizeof
abbreviate sta static
abbreviate str struct
abbreviate sw switch
abbreviate ty typedef
abbreviate un unsigned
abbreviate ui unsigned int
abbreviate ul unsigned long
abbreviate u3 u32
abbreviate u4 u64
abbreviate vo volatile
abbreviate wh while

"Set gvim options
"set cindent
set nobackup
"set nowrapscan
set autoindent
" Reads changed files automatically. Dangerous??
set autoread
autocmd CursorHold * checktime
set autowriteall
set backupdir=/tmp
set cinoptions+=l1
set cinoptions+=t0
set cinoptions+=:0
set noexpandtab
set gdefault
set hlsearch
set ignorecase
set incsearch
set noeol
set nu
set ruler
set scrolloff=3
set shiftwidth=8
set showcmd
set smartcase
set smartindent
set softtabstop=8
set switchbuf=usetab
set ts=8
set wildignore=*.o,*.swp,*.bak,*.pyc
set wildignorecase
set wildmode=list:longest
set winaltkeys=no
set writebackup

let loaded_matchparen = 1

set tags=tags
set path=drivers/scsi/bnx2fc,.,include
"set diffopt+=iwhite
set guioptions-=T
set cscopequickfix=s-,c-,d-,i-,t-,e-,g-
set cscopetag
set csto=1
"noremap <C-g> <C-]>
set nocscopeverbose
"set textwidth=100

" Remove scrollbars
set guioptions-=L
set guioptions-=r
set guioptions+=m
set showtabline=2

let g:locateopen_ignorecase = 1

"Alphabet Alt Mappings
noremap <M-a> :!cscope -bv<CR>:cs r<CR><CR>
"noremap <M-b> :FufBuffer<C-m>
noremap <M-b> :CommandTBuffer<CR>
noremap <M-c> I/*<Esc>A*/<Esc>
noremap <M-d> ^xx$xx
noremap <M-e> :cs find e 
noremap <M-f> :wa<CR>
noremap <M-g> :cs find g 
noremap <M-i> zc
noremap <M-k> ddkA<Space>{<C-m>}<Esc>kpo
noremap <M-l> [{zf%
noremap <M-m> :make<CR>
nnoremap <M-n> :noh<CR>
noremap <M-o> zo
noremap <M-p> :colder<CR>
noremap <M-r> ddkA<Space>{<C-m>}<Esc>kpO
noremap <M-s> :cs find s 
noremap <M-t> :TlistToggle<C-m><C-w>h
noremap <M-u> :mksession! .gvimsession<CR>
noremap <M-w> @q
nmap <C-n> :set invnumber<C-m>


" Tab mappings
nmap <M-1> 1gt
nmap <M-2> 2gt
nmap <M-3> 3gt
nmap <M-4> 4gt
nmap <M-5> 5gt
nmap <M-6> 6gt
nmap <M-7> 7gt
nmap <M-8> 8gt
nmap <M-9> 9gt
nmap <M-0> 10gt

" Jump to header/source
nmap ,s :find %:t:r.c<CR>
nmap ,h :find %:t:r.h<CR>
nmap Y y$

noremap <C-t> :tabnew<CR>

"Non Alphabet Alt Mappings
noremap <M-]> <C-]>z<C-m>
noremap <M-[> <C-t>
noremap <M-.> :cn<C-m>
noremap . :cn<CR>
noremap <M-,> :cp<C-m>
noremap , :cp<CR>
noremap <M-=> 20==
noremap <M-Space> <C-u>


"Alphabet Ctrl Mappings
noremap <C-d> :bd<C-m>
"noremap <C-f> :FF<C-m><C-x><C-o>
"noremap <C-f> :FufCoverageFileRegister<CR>.fufcache/*<CR><Esc>f<CR>:FufCoverageFileChange f<CR>
noremap <C-f> :CommandT<CR>
noremap <C-h> <C-w>h
noremap <C-j> <C-w>j
noremap <C-k> <C-w>k
noremap <C-l> <C-w>l
"noremap <C-o> <C-T>
noremap <C-q> :q<C-m>
"noremap <C-w> :set diffopt+=iwhite<C-m>

fun! ReadMan()
  " Assign current word under cursor to a script variable:
  let s:man_word = expand('<cword>')
  " Open a new window:
  :exe ":wincmd n"
  " Read in the manpage for man_word (col -b is for formatting):
  :exe ":r!man " . s:man_word . " | col -b"
  " Goto first line...
  :exe ":goto"
  " and delete it:
  :exe ":delete"
endfun

function! ViewMan()
	let s:man_word = expand("<cword>")
	:exe ":tabnew"
	:exe ":Man " . s:man_word
	:exe ":only"
endfun

"Alphabet Shift Mappings
noremap <S-f> :FufFileWithCurrentBufferDir<CR>
noremap <S-k> :call ViewMan()<CR>

"cscope remappings
noremap <C-c> :cs find c <C-R>=expand("<cword>")<CR><CR>
"noremap <C-d> :cs find d <C-R>=expand("<cword>")<CR><CR>
noremap <C-e> :cs find e <C-R>=expand("<cword>")<CR><CR>
noremap <C-g> :cs find g <C-R>=expand("<cword>")<CR><CR>
noremap <C-s> :cs find s <C-R>=expand("<cword>")<CR><CR>

"Misc Mappings
noremap <Space> <C-d>
noremap ' `
noremap fl 0f"a\n%s.%s.%d\n:<Space><Esc>f"a,<Space>__func__,<Space>__FILE__,<Space>__LINE__<Esc>
"Swap ; and :
nnoremap ; :
nnoremap : ;

inoremap <S-Tab> <Tab>
inoremap <Esc>[Z <Tab>
inoremap { <Space>{<CR>
inoremap } <CR>}
inoremap <M-[> {
inoremap [  {
inoremap <M-]> }
inoremap ] }
inoremap fj <Esc>

inoremap <M-c> <C-c>a
inoremap <M-k> <C-y>
inoremap <M-l> <C-c>a<Space>
inoremap <M-m> <Esc>:make<CR>
inoremap <M-q> /*  */<Esc>hhi
"inoremap <M-.> <Esc>bywi<< "<Esc>A:<Space>"<Space><<<Space><Esc>pA<Space>

" Complete local buffer on 1st tab. Scroll through list when menu visible
" inoremap <Tab> <C-R>=pumvisible() ? "\<lt>C-p>" : "\<lt>C-x>\<lt>C-p>"<CR>

" Tab completion is working with menu with C-p. Update this with details when it's not
inoremap <Tab> <C-p>

"Set tab complete to local complete
"inoremap <Tab> <C-x><C-p>

"inoremap fdb<Space> FCM_LOG_DBG("== [%s]: ", p->ifname);<Esc>13hi
"inoremap ner<Space> netdev_err(tp->dev, "== [%s@%s:%d]\n", __func__, __FILE__, __LINE__);<Esc>34hi
inoremap psf<Space> printf("@@ [%s@%s:%d]\n", __func__, __FILE__, __LINE__);<Esc>34hi
inoremap prk<Space> printk(KERN_ERR "
inoremap psk<Space> printk(KERN_ERR "@@ [%s:%d]\n", __func__, __LINE__);<Esc>24hi
inoremap psl<Space> printk_ratelimited(KERN_ERR "@@ [%s@%s:%d]\n", __func__, __FILE__, __LINE__);<Esc>34hi


inoremap <M-Space> <C-c>a<Space>

vnoremap <M-j> <Esc>
vnoremap <M-c> d<Esc>i#if 0<C-m>#endif<C-m><Esc>kkp
vnoremap <M-f> d<Esc>i#ifdef CONFIG_TINTRI<C-m>#endif<C-m><Esc>kkp
vnoremap <M-d> %dd''dd
vnoremap fj <Esc>

"set guifont=7x14
"set guifont=Monospace\ 10
"set guifont=Liberation\ Mono\ 9.4
set guifont=Liberation\ Mono\ 11

runtime ftplugin/man.vim

"Hilighting
colorscheme summerfruit256
"colorscheme zellner

hi Pmenu          guifg=white     guibg=#808080
hi PmenuSel       guifg=black     guibg=#ffbc29


"autocmds
"autocmd GUIENTER * winpos 1925 0
"autocmd GUIENTER * set lines=64 columns=265
autocmd BufRead,BufNewFile *.c,*.cpp,*.h set cindent
autocmd BufRead,BufNewFile *.c,*.cpp,*.h set noexpandtab

filetype on
filetype plugin on
filetype indent on

set completeopt=menu,longest,preview

" Style Errors
highlight TrailSpace ctermbg=LightRed ctermfg=white guibg=LightRed guifg=white
highlight SpcTab ctermbg=LightBlue ctermfg=white guibg=LightBlue guifg=white
highlight OverLength ctermbg=Red ctermfg=white guibg=Red guifg=white

autocmd BufWinEnter,BufCreate,BufRead *.c,*.h match SpcTab / \+	/

if version >= 703
	autocmd BufWinEnter,BufCreate,BufRead *.c,*.h highlight colorcolumn ctermbg=LightCyan guibg=LightCyan ctermfg=Black guifg=Purple
endif

autocmd BufWinEnter,BufCreate,BufRead *.c,*.h 3match TrailSpace /\s\+$/

autocmd InsertEnter *.c,*.h 3match TrailSpace /\s\+\%#\@<!$/
autocmd InsertLeave *.c,*.h 3match TrailSpace /\s\+$/
autocmd BufWinLeave call clearmatches()

autocmd BufWinEnter,BufCreate,BufRead *.cpp,*.java set softtabstop=4
autocmd BufWinEnter,BufCreate,BufRead *.cpp,*.java set tabstop=4
autocmd BufWinEnter,BufCreate,BufRead *.cpp,*.java set shiftwidth=4
autocmd BufWinEnter,BufCreate,BufRead *.cpp,*.java set expandtab

autocmd BufWinLeave *.cpp,*.java set softtabstop=8
autocmd BufWinLeave *.cpp,*.java set tabstop=8
autocmd BufWinLeave *.cpp,*.java set shiftwidth=8
autocmd BufWinLeave *.cpp,*.java set noexpandtab

if version >= 703
	autocmd BufWinEnter,BufCreate,BufRead *.c,*.h,*.cpp,*.java set colorcolumn=81
endif

autocmd BufWinEnter,BufCreate,BufRead *.c,*.h 2match OverLength /\%81v.*/

autocmd BufWinEnter,BufCreate,BufRead RELEASE.TXT set expandtab
autocmd BufWinEnter,BufCreate,BufRead ChangeLog set expandtab


" ==============================================================================
" Save windows size/position
if has("gui_running")
  function! ScreenFilename()
    if has('amiga')
      return "s:.vimsize"
    elseif has('win32')
      return $HOME.'\_vimsize'
    else
      return $HOME.'/.vimsize'
    endif
  endfunction

  function! ScreenRestore()
    " Restore window size (columns and lines) and position
    " from values stored in vimsize file.
    " Must set font first so columns and lines are based on font size.
    let f = ScreenFilename()
    if has("gui_running") && g:screen_size_restore_pos && filereadable(f)
      let vim_instance = (g:screen_size_by_vim_instance==1?(v:servername):'GVIM')
      for line in readfile(f)
        let sizepos = split(line)
        if len(sizepos) == 5 && sizepos[0] == vim_instance
          silent! execute "set columns=".sizepos[1]." lines=".sizepos[2]
          silent! execute "winpos ".sizepos[3]." ".sizepos[4]
          return
        endif
      endfor
    endif
  endfunction

  function! ScreenSave()
    " Save window size and position.
    if has("gui_running") && g:screen_size_restore_pos
      let vim_instance = (g:screen_size_by_vim_instance==1?(v:servername):'GVIM')
      let data = vim_instance . ' ' . &columns . ' ' . &lines . ' ' .
            \ (getwinposx()<0?0:getwinposx()) . ' ' .
            \ (getwinposy()<0?0:getwinposy())
      let f = ScreenFilename()
      if filereadable(f)
        let lines = readfile(f)
        call filter(lines, "v:val !~ '^" . vim_instance . "\\>'")
        call add(lines, data)
      else
        let lines = [data]
      endif
      call writefile(lines, f)
    endif
  endfunction

  if !exists('g:screen_size_restore_pos')
    let g:screen_size_restore_pos = 1
  endif
  if !exists('g:screen_size_by_vim_instance')
    let g:screen_size_by_vim_instance = 0
  endif
  autocmd VimEnter * if g:screen_size_restore_pos == 1 | call ScreenRestore() | endif
  autocmd VimLeavePre * if g:screen_size_restore_pos == 1 | call ScreenSave() | endif
endif


noremap <C-p> :QFix<C-m>

if (filereadable(glob("~/.gvimrc_local")))
	source ~/.gvimrc_local
endif

if (filereadable(glob(".gvimrc_")))
	source .gvimrc_
endif


let s:pattern = '^\(.* \)\([1-9][0-9]*\)$'
let s:minfontsize = 6
let s:maxfontsize = 16
function! AdjustFontSize(amount)
  if has("gui_gtk2") && has("gui_running")
    let fontname = substitute(&guifont, s:pattern, '\1', '')
    let cursize = substitute(&guifont, s:pattern, '\2', '')
    let newsize = cursize + a:amount
    if (newsize >= s:minfontsize) && (newsize <= s:maxfontsize)
      let newfont = fontname . newsize
      let &guifont = newfont
    endif
  else
    echoerr "You need to run the GTK2 version of Vim to use this function."
  endif
endfunction

function! LargerFont()
  call AdjustFontSize(1)
endfunction
command! LargerFont call LargerFont()

function! SmallerFont()
  call AdjustFontSize(-1)
endfunction
command! SmallerFont call SmallerFont()

" Make alt mappings work in console vim
let c='a'
while c <= 'z'
  exec "set <A-".c.">=\e".c
  exec "imap \e".c." <A-".c.">"
  let c = nr2char(1+char2nr(c))
endw

let c='1'
while c <= '9'
  exec "set <A-".c.">=\e".c
  exec "imap \e".c." <A-".c.">"
  let c = nr2char(1+char2nr(c))
endw

set timeout ttimeoutlen=50

if &term =~ "xterm\\|rxvt"
  " use an blue cursor in insert mode
  let &t_SI = "\<Esc>]12;orange\x7"
  " use a red cursor otherwise
  let &t_EI = "\<Esc>]12;green\x7"
  " reset cursor when vim exits
  autocmd VimLeave * silent !echo -ne "\033]112\007"
endif

