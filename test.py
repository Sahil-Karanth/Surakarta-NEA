import tkinter as tk

root = tk.Tk()

# Create the buttons


buttons_left = []
for i in range(1,6):
    button = tk.Button(root, text=f"Button {i}")
    buttons_left.append(button)
    button.grid(row=i, column=0, padx=10, pady=10)

buttons_right = []
for i in range(1,6):
    button = tk.Button(root, text=f"Button {i}")
    buttons_right.append(button)
    button.grid(row=i, column=1, padx=10, pady=10)

# Center the grid within the window
root.geometry("+%d+%d" % ((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2,
                          (root.winfo_screenheight() - root.winfo_reqheight()) / 2))

root.mainloop()