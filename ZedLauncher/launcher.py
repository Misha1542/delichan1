import tkinter as tk
root = tk.Tk() 
class OOP:
  def __init__(self, text, ekran):
    self.text = text
    self.ekran = ekran
  def create_label(self):
         name = tk.Label(self.ekran, text=self.text)
         name.pack()
    
jopa = OOP(text="жопа", ekran=root)
jopa.create_label()
root.mainloop()
