from PIL import Image, ImageDraw, ImageFont

# Get user input text
user_text = input("Enter the text you want to convert to an image: ")

# Set up image dimensions
width, height = 400, 200
background_color = (255, 255, 255)  # White

# Create a new image
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Load a font (you can change the font and font size as desired)
font_size = 30
font = ImageFont.truetype("arial.ttf", font_size)

# Calculate text size and position
text_width, text_height = draw.textsize(user_text, font=font)
x_position = (width - text_width) // 2
y_position = (height - text_height) // 2

# Draw the text on the image
text_color = (0, 0, 0)  # Black
draw.text((x_position, y_position), user_text, font=font, fill=text_color)

# Save the image
image.save("text_image.png")
print("Image saved as 'text_image.png'")
