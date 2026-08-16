import tkinter as tk
root = tk.Tk() 
class OOP:
  def __init__(self, name, text):
    self.name = name
    self.text = text
  def create_label(self):
    self.name = tk.Label(text=self.text)
    self.name.pack()
jopa = OOP('label', 'жопа')
root.mainloop()
