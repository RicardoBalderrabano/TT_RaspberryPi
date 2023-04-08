'''
This Script is an example of a GUI made with kivy
Shows 1 button and when it is preessed 3 buttons are deployed 
The button and layout configuration is in the file sd.kv
'''


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder


# Designate the .kv design file
Builder.load_file('sd.kv')

class MyLayout(Widget):
    def spinner_clicked(self, value):
            self.ids.click_label.text==value

class AwesomeApp(App):
    def build(self):
            return MyLayout()
        

if __name__=='__main__':
    AwesomeApp().run()
   

    
                   
    