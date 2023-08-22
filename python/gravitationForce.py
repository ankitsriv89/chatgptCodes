import tkinter as tk
from tkinter import ttk

def calculate_force():
    try:
        mass1 = float(entry_mass1.get())
        mass2 = float(entry_mass2.get())
        distance = float(entry_distance.get())

        gravitational_constant = 6.67430e-11  # m^3 kg^-1 s^-2

        force = (gravitational_constant * mass1 * mass2) / (distance ** 2)
        label_result.config(text=f"Gravitational Force: {force:.2e} N")
    except ValueError:
        label_result.config(text="Please enter valid values.")

# Create the main window
root = tk.Tk()
root.title("Gravitational Force Calculator")

# Labels
label_mass1 = ttk.Label(root, text="Mass of Object 1 (kg):")
label_mass2 = ttk.Label(root, text="Mass of Object 2 (kg):")
label_distance = ttk.Label(root, text="Distance (m):")
label_result = ttk.Label(root, text="")

# Entry fields
entry_mass1 = ttk.Entry(root)
entry_mass2 = ttk.Entry(root)
entry_distance = ttk.Entry(root)

# Calculate button
button_calculate = ttk.Button(root, text="Calculate", command=calculate_force)

# Place widgets on the grid
label_mass1.grid(row=0, column=0, padx=10, pady=10)
entry_mass1.grid(row=0, column=1, padx=10, pady=10)
label_mass2.grid(row=1, column=0, padx=10, pady=10)
entry_mass2.grid(row=1, column=1, padx=10, pady=10)
label_distance.grid(row=2, column=0, padx=10, pady=10)
entry_distance.grid(row=2, column=1, padx=10, pady=10)
button_calculate.grid(row=3, columnspan=2, padx=10, pady=10)
label_result.grid(row=4, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
