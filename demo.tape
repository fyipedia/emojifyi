# emojifyi — Python Emoji Metadata Library Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 580
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with emojifyi python3"
Enter
Sleep 2.5s

Type "from emojifyi import lookup, search, encode"
Enter
Sleep 1s

Type "# Look up emoji by character"
Enter
Sleep 0.5s

Type "lookup('🎉')['name']"
Enter
Sleep 1.5s

Type "# Search emojis by keyword"
Enter
Sleep 0.5s

Type "[e['char'] for e in search('fire')[:5]]"
Enter
Sleep 2s

Type "exit()"
Enter
Sleep 1s
