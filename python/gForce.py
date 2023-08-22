import tkinter as tk
from tkinter import messagebox

def calculate_gravitational_force():
    try:
        mass1 = float(entry_mass1.get())
        mass2 = float(entry_mass2.get())
        distance = float(entry_distance.get())
        
        gravitational_constant = 6.67430e-11
        force = (gravitational_constant * mass1 * mass2) / (distance ** 2)
        
        result_label.config(text=f"Gravitational Force: {force:.2e} N")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Create the main GUI window
root = tk.Tk()
root.title("Gravitational Force Calculator")

# Labels and entry fields
label_mass1 = tk.Label(root, text="Mass 1 (kg):")
entry_mass1 = tk.Entry(root)

label_mass2 = tk.Label(root, text="Mass 2 (kg):")
entry_mass2 = tk.Entry(root)

label_distance = tk.Label(root, text="Distance (m):")
entry_distance = tk.Entry(root)

calculate_button = tk.Button(root, text="Calculate Force", command=calculate_gravitational_force)
result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))

# Grid layout
label_mass1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_mass1.grid(row=0, column=1, padx=10, pady=5)

label_mass2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_mass2.grid(row=1, column=1, padx=10, pady=5)

label_distance.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_distance.grid(row=2, column=1, padx=10, pady=5)

calculate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
