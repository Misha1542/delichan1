import tkinter as tk
root = tk.Tk() 
class OOP:
  def __init__(self, text, ekran):
    self.text = text
    self.ekran = ekran
  def create_label(self):
    self.name = tk.Label(self.ekran, text=self.text)
    self.name.pack()
    
jopa = OOP(text="жопа", ekran=root)
jopa.create_label()
root.mainloop()
