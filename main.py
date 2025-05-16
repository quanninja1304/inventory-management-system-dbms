import ttkbootstrap as ttk
from controller import Controller

if __name__ == "__main__":
    root = ttk.Window()  # Use "flatly" to avoid litera issues; revert to "litera" if resolved
    app = Controller(root)
    root.mainloop()