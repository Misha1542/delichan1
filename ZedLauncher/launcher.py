import tkinter as tk
root = tk.Tk() 
class OOP:
  def __init__(self, name, text, ekran):
    self.name = name
    self.text = text
    self.ekran = ekran
  def create_label(self):
    self.name = tk.Label(self.ekran, text=self.text)
    self.name.pack()
    
jopa = OOP(name= "label", text="жопа", ekran=root)
jopa.create_label()
root.mainloop()
