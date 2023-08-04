import cv2
import tkinter as tk
from tkinter import filedialog

def resize_image(image, max_dimension=800):
    height, width = image.shape[:2]
    if max(height, width) > max_dimension:
        scale_factor = max_dimension / max(height, width)
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)
        return cv2.resize(image, (new_width, new_height))
    return image

def convert_to_sketch(image_path):
    # Read the input image
    original_image = cv2.imread(image_path)

    # Resize the image if needed to fit on the screen
    resized_image = resize_image(original_image)

    # Convert the resized image to grayscale
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray_image = 255 - gray_image

    # Apply a blur to the inverted image using the GaussianBlur function
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)

    # Invert the blurred image
    inverted_blurred_image = 255 - blurred_image

    # Create the sketch by blending the original image and the inverted, blurred image
    sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

    return sketch

def save_sketch(sketch_image):
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")])
    if save_path:
        cv2.imwrite(save_path, sketch_image)
        print("Sketch saved successfully.")

def main():
    root = tk.Tk()
    root.title("Image to Sketch Converter")

    # Replace 'input_image.jpg' with the path to your input image
    input_image_path = 'slamdunk.jpg'

    # Convert the image to a sketch
    sketch_image = convert_to_sketch(input_image_path)

    # Show the original and sketch images side by side
    cv2.imshow('Original Image', resize_image(cv2.imread(input_image_path)))
    cv2.imshow('Sketch Image', sketch_image)
    cv2.waitKey(0)  # Wait for a key press to close the image windows

    def on_save_button():
        save_sketch(sketch_image)

    save_button = tk.Button(root, text="Save Sketch", command=on_save_button)
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
