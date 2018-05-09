import kivy
kivy.require('1.10.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

__author__ = 'WellenWoo'

Builder.load_file('morse.kv')

Keys = 'abcdefghijklmnopqrstuvwxyz0123456789'
Values = ['.-','-...','-.-.','-..','.','..-.','--.','....',
          '..','.---','-.-','.-..','--','-.','---','.--.',
          '--.-','.-.','...','-', '..-','...-','.--','-..-',
          '-.--','--..','-----','.----','..---','...--',
          '....-','.....','-....','--...','---..','----.']
CODE = dict(zip(Keys.upper(), Values))

Decode_value = CODE.keys()
Decode_key = CODE.values()
Decode_dict = dict(zip(Decode_key,Decode_value))

class Morse(FloatLayout):
    def Decode(self):

        msg = self.ids["input"].text
        msg1 = msg.split()
        temp = []
        for s in msg1:
            if s in Decode_dict.keys():
                temp.append(Decode_dict[s])
        ans = str(temp)
        self.ids.output.text = ans

    def Encode(self):
        msg = self.ids["input"].text
        temp = []
        for s in msg:
            if s == ' ':
                temp.append('')
            else:
                temp.append(CODE[s.upper()] + '   ')
        ans = str(temp)
        ans = ans.replace('\'','')
        ans = ans.replace(',',' ')
        self.ids["output"].text = ans

class MainFrame(App):

    def build(self):
        return Morse()

    def on_stop(self):
        return True

if __name__ == '__main__':
    MainFrame().run()
