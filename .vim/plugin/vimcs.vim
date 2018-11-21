function! s:edit_path(path)
  execute "edit " . <SID>add_depot_root(a:path)
endfunction

function! s:citcroot()
  return matchstr(getcwd(), '^/google/src/cloud/[^/]\+/[^/]\+/')
endfunction

function! s:add_depot_root(path)
  if <SID>in_citc()
    return <SID>citcroot() . a:path
  else
    return "/google/src/files/head/depot" . a:path
  endif
endfunction

function! s:in_citc()
  return match(getcwd(), '^/google/src/cloud/') != -1
endfunction

function! s:csearch(search)
  let b:root='/google/src/files/head/depot'
  if <SID>in_citc()
    let b:root=<SID>citcroot()
  endif

  call fzf#run({
    \ 'source': "csearch -l " . a:search . "| sed 's|^/google/src/files/head/depot||'",
    \ 'sink': function("s:edit_path"),
    \ 'options': '-m --preview-window=up:65% --preview="cat ' . b:root . '{}"'
    \ })
endfunction

command! -nargs=+ CSearch :call <SID>csearch("<args>")
cnoreabbrev cs CSearch
