import webbrowser as wbb
words = command.split()
if len(words) < 2:
    words = [1,'']
wbb.get().open_new_tab('https://www.google.com/search?q=' + '%20'.join(words[1:]))