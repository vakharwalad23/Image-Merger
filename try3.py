import os
import tempfile
import requests
from PIL import Image
from backgroundremover import bg as BackgroundRemover

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
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                    temp.write(image_bytes)
                    temp_filename = temp.name

                # You can also use 'u2netp' or 'u2net_human_seg'
                remover = BackgroundRemover
                remover.remove(
                    temp_filename, temp_filename + "_no_bg.png")

                img = Image.open(temp_filename + "_no_bg.png")
                output_images.append(img)

                os.remove(temp_filename)
                os.remove(temp_filename + "_no_bg.png")

            except Exception as e:
                print(f"Error processing image from {url}: {e}")

    if not output_images:
        print("No images processed successfully.")
        return

    new_image = Image.new('RGBA', output_images[0].size)

    offset_x = 0
    for img in output_images:
        new_image.paste(img, (offset_x, 0), img)
        offset_x += img.width // 5
    new_image.save(output_path, 'PNG')


remove_background_and_overlay(image_urls, output_path)
