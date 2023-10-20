from removebg import RemoveBg
from PIL import Image
import os
import tempfile
import requests

image_urls = [
    'https://cdn.grofers.com/app/images/products/full_screen/pro_574.jpg?ts=1684834987',
    'https://cdn.grofers.com/app/images/products/full_screen/pro_578.jpg?ts=1685979257',
    'https://cdn.grofers.com/app/images/products/full_screen/pro_240092.jpg?ts=1685979820'
]
output_path = 'output.png'
api_key = "Zc2ifE5u4Duirh6W6dRSHYAr"


def remove_background_and_overlay(image_urls, output_path):
    rmbg = RemoveBg(api_key, "error.log")
    output_images = []

    for url in image_urls:
        image_bytes = requests.get(url).content
        if image_bytes:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
                    temp.write(image_bytes)
                    temp_filename = temp.name

                rmbg.remove_background_from_img_file(temp_filename)

                result_filename = temp_filename + "_no_bg.png"

                img = Image.open(result_filename)
                output_images.append(img)

                os.remove(temp_filename)
                os.remove(result_filename)

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
