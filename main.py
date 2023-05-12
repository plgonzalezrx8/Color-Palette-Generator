import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from sklearn.cluster import KMeans

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

def get_image_colors(image_path, num_colors):
    # Load image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Convert image to RGB mode
    image = image.resize((500, 500))  # Resize the image to reduce processing time

    # Convert image into an array of RGB values
    image_array = np.array(image)
    image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))

    # Use KMeans clustering to find the dominant colors
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(image_array)

    # Get the RGB values of the dominant colors
    dominant_colors_rgb = kmeans.cluster_centers_.astype(int)
    dominant_colors_hex = [rgb_to_hex(color) for color in dominant_colors_rgb]

    return dominant_colors_rgb, dominant_colors_hex

def save_color_palette(dominant_colors_rgb, dominant_colors_hex, output_path):
    # Create an image to display the color palette
    palette_image = Image.new('RGB', (100 * len(dominant_colors_rgb), 100))
    draw = ImageDraw.Draw(palette_image)
    font = ImageFont.truetype('arial.ttf', 14)

    for index, color in enumerate(dominant_colors_rgb):
        for y in range(100):
            for x in range(100):
                palette_image.putpixel((index * 100 + x, y), tuple(color))

        draw.text((index * 100 + 5, 75), dominant_colors_hex[index], fill=(255, 255, 255), font=font)

    palette_image.save(output_path)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python color_palette.py <input_image> <num_colors> <output_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    num_colors = int(sys.argv[2])
    output_image = sys.argv[3]

    dominant_colors_rgb, dominant_colors_hex = get_image_colors(input_image, num_colors)
    save_color_palette(dominant_colors_rgb, dominant_colors_hex, output_image)

    print("Dominant colors (HEX):")
    for color in dominant_colors_hex:
        print(color)