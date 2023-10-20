import jimp from 'jimp';
import axios from 'axios';

const imageUrls = [
  'https://cdn.grofers.com/app/images/products/full_screen/pro_574.jpg?ts=1684834987',
  'https://cdn.grofers.com/app/images/products/full_screen/pro_578.jpg?ts=1685979257',
  'https://cdn.grofers.com/app/images/products/full_screen/pro_240092.jpg?ts=1685979820',
];
const outputFilePath = 'output.png';

const removeBackgroundAndOverlay = async (imageUrls, outputFilePath) => {
  const outputImages = [];

  for (const url of imageUrls) {
    try {
      const response = await axios.get(url, { responseType: 'arraybuffer' });
      const imageBuffer = response.data;

      const image = await jimp.read(imageBuffer);
      image.quality(100).background(0xFFFFFFFF).opaque();
      image.scan(0, 0, image.bitmap.width, image.bitmap.height, function (x, y, idx) {
        const red = this.bitmap.data[idx + 0];
        const green = this.bitmap.data[idx + 1];
        const blue = this.bitmap.data[idx + 2];
      
        if (red > 200 && green > 200 && blue > 200) {
          this.bitmap.data[idx + 3] = 0;
        }
        else if (red > 150 && green > 150 && blue > 150) {
          this.bitmap.data[idx + 3] = 255;
        }
      });
      outputImages.push(image);
    } catch (error) {
      console.error(`Error processing image from ${url}: ${error}`);
    }
  }

  if (outputImages.length === 0) {
    console.log('No images processed successfully.');
    return;
  }

  const newImage = new jimp(outputImages[0].bitmap.width * outputImages.length, outputImages[0].bitmap.height);

  let offsetX = 0;
  for (const img of outputImages) {
    newImage.blit(img, offsetX, 0);
    offsetX += img.bitmap.width / 5;
  }

  newImage.write(outputFilePath);
};

removeBackgroundAndOverlay(imageUrls, outputFilePath);
