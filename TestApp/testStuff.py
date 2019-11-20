from PIL import Image

img = Image.open("quit_button.png")
img = img.resize((30, 30))
print(img.size)