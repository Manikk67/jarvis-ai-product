from PIL import Image

img = Image.open("jarvis.png")

img.save(
    "jarvis.ico",
    format="ICO",
    sizes=[(256, 256)]
)

print("✅ jarvis.ico created successfully")