import tkinter as tk
from tkinter import scrolledtext, Button
from PIL import Image, ImageDraw, ImageFont

def convert_to_image():
    user_input = text_area.get("1.0", "end-1c")  # Get user input from textarea
    
    # Create an image
    image = Image.new("RGB", (400, 300), "white")
    draw = ImageDraw.Draw(image)
    
    # Define font
    font = ImageFont.load_default()  # You can also provide a font file path
    
    # Calculate text size and position
    text_width, text_height = draw.textsize(user_input, font=font)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2
    
    # Draw text on the image
    draw.text((x, y), user_input, fill="black", font=font)
    
    # Save the image
    image.save("user_input_image.png")
    print("Image saved as user_input_image.png")

# Create the main window
root = tk.Tk()
root.title("Text to Image Converter")

# Create a textarea for user input
text_area = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
text_area.pack(padx=10, pady=10)

# Create a button to trigger conversion
convert_button = Button(root, text="Convert to Image", command=convert_to_image)
convert_button.pack()

# Start the GUI event loop
root.mainloop()
