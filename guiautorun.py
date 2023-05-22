import PySimpleGUI as sg 

layout = [[sg.Text('GUI Autorun at Startup', font=("Helvatica", 30))],
[sg.Text('It works! Click Exit to go to the desktop.', font=("Calibri", 20))],
[sg.Exit()]]

window = sg.Window('GUI Autorun', layout, size=(1024, 600), element_justification="center", finalize=True)
window.Maximize()

while True:
    event, values =window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()