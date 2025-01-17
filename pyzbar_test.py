from PIL import Image

# Specify the image file name
image_path = "ricekrispies.png"

try:
    # Load the image
    img = Image.open(image_path)
    print("Image loaded successfully!")
except FileNotFoundError:
    print(f"Error: File '{image_path}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
from pyzbar.pyzbar import decode
from PIL import Image

# Path to the barcode image
image_path = "ricekrispies.png"  # Replace with your image name

try:
    # Load the image
    img = Image.open(image_path)
    print("Image loaded successfully!")
except FileNotFoundError:
    print(f"Error: File '{image_path}' not found.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Decode the barcode
decoded_objects = decode(img)

# Print the decoded results
if decoded_objects:
    for obj in decoded_objects:
        print(f"Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
else:
    print("No barcodes found in the image.")
python3.py