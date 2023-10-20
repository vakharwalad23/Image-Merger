from PIL import Image
import requests
import cv2
import numpy as np

image_urls = [
    'https://cdn.grofers.com/app/images/products/full_screen/pro_574.jpg?ts=1684834987',
    'https://cdn.grofers.com/app/images/products/full_screen/pro_578.jpg?ts=1685979257',
    'https://cdn.grofers.com/app/images/products/full_screen/pro_240092.jpg?ts=1685979820'
]
output_path = 'output.png'


def remove_background_and_overlay(image_urls, output_path):
    output_images = []

    for url in image_urls:
        image_bytes = requests.get(url).content
        if image_bytes:
            try:
                # Load the image using OpenCV
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Convert the image to RGBA format
                img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

                # Define a mask for the background (white) and the object (black)
                lower_white = np.array([200, 200, 200, 0], dtype=np.uint8)
                upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)
                mask = cv2.inRange(img_rgba, lower_white, upper_white)

                # Invert the mask to keep the object and remove the background
                mask = cv2.bitwise_not(mask)

                # Apply the mask to the image
                img_rgba[mask != 0] = [0, 0, 0, 0]

                # Convert the image back to PIL format
                img_pil = Image.fromarray(img_rgba)

                output_images.append(img_pil)

            except Exception as e:
                print(f"Error processing image from {url}: {e}")

    if not output_images:
        print("No images processed successfully.")
        return

    new_image = Image.new('RGBA', output_images[0].size)

    offset_x = 0
    for img in output_images:
        new_image.paste(img, (offset_x, 0), img)
        offset_x += img.width // 2

    new_image.save(output_path, 'PNG')


remove_background_and_overlay(image_urls, output_path)
