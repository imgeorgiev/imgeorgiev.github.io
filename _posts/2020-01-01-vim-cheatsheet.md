# Vim cheatsheet

## Modes

- Normal mode - for navigating files
- Insert mode - for adding text
- Visual mode - for highlighting where you are at
- Visual block mode - ?

## Commands
:w - writes
:q - quits
:e - edits
:e! - reload file from disk
:123 - goes to line 123
:r file.txt - read file into current file
:abb a b - set acronym; when you write a, vim automatically makes it b
:! ls - executes ls and other bash commands in your terminal
:com! py ! python % - maps :py to running a python command in a terminal straight from vim

## Buffers

:bd - delete current buffer
:bn - next buffer
:bp - previous buffer
:b file.txt - swtich buffer to a particular one
:ls - check currently open buffers

## Tabs

:tabedit file.md - opens a new file in a tab
:tabfind file.md - recuvrsively find a file
:0tabnew - opens a new tab in position 0
gt - goes to next tab
gT - goes to prev tab
[i]gt - goes to tab i
:tabm - moves curent tab to final position
:tabm +2 - move current tab 2 places forward
:tabm 0 - moves to current tab to tab place 0
:tabs - displays currently open tabs
:tabc - closes current tab
:tabo - closes all tabs except the current one

## Splits and windows
:split - splits the current window into two
Ctrl+w + w - cycle windows
Ctrl-w + c - close window
:diffsplit file2 - opens file2 in diff mode

## Navigation
h,j,k,l - navigates the file like arrowkeys
i - enter insert mode
o - enter insert mode on line below
O - enter intert mode on line above
w - goes to next word
e - goes to end of current word
W - goes to the next word including all characters except space, tab and EOL
E - goes to the end of the current word including all characters except space, tab and EOL
() - goes to previous or next sentance
{} - goes to previous or next paragraph
gg - goes to beginning of file
G - goes to end of file
Ctrl+f - pagedown
Ctrl+b - pageup
$ - goes to end of line
0 - goes to begging of line
* - searches for word under cursor
d - delete; dw deletes a word
dd - delete line
u - undo change
U - undo whole line of changes
y - copy/yank
yy - copy line
p - paste
Shift+p - paste before cursor
x - cut
r - replace character under cursor
R - replace indefinately
c - change (i.e. delete something and go into insert mode); cw - delete word and insert mode
"a - select copy/paste buffer a; can use any letter on the keyboard to access all 52 buffers
ma - defines mark 'a'; can be anything
'a - return to mark 'a'; can be anything
'. - return to last change; . is a special mark
Ctrl+o - go back to last cursor jump
Ctrl+i - go to the next cursor jump
gf - go to file under cursor
% - go to matching bracket

## Searching

/someword - searches for someword (and supports regex)
?someword - searches for someward backwards
n - next word
N - prev word
Ctrl+O - go back where you came from
:s/you/they - replaces you with they
:s/you/they/g - replaces you with they for whole line
:10,20s/you/they/g - replaces you with they for all lines between 10 and 20
:%s/old/new/g - replaces old with new for the whole file
:%s/old/new/gc - replaces old with new for the whole file with a prompt for each replace

## Others

vim -d file1 file2 - opens vim in diff mode to compare 2 files

