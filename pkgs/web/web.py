import webbrowser as wbb

if len(command.split()) < 2:
    print('Usage: web <URL>')
else:
    wbb.get().open_new_tab(command.split()[1])