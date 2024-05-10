from PIL import Image
import os
from tkinter import Tk, filedialog

def get_image_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff'), ('All files', '*.*')]
    )
    return file_path

def generate_tiles(image_path, output_folder, tile_size=256):
    image = Image.open(image_path)
    width, height = image.size

    # Определяем максимальный уровень зума
    max_zoom_level = 0
    while (tile_size * (2 ** max_zoom_level) < max(width, height)):
        max_zoom_level += 1

    # Создаем тайлы для каждого уровня масштабирования
    for zoom in range(max_zoom_level + 1):
        num_tiles = 2 ** zoom
        zoom_folder = os.path.join(output_folder, str(zoom))
        os.makedirs(zoom_folder, exist_ok=True)

        # Масштабируем исходное изображение для текущего уровня зума
        scale_factor = 1 / (2 ** (max_zoom_level - zoom))
        scaled_width = int(width * scale_factor)
        scaled_height = int(height * scale_factor)
        scaled_img = image.resize((scaled_width, scaled_height), Image.LANCZOS)

        # Создаем тайлы для текущего уровня масштабирования
        for x in range(num_tiles):
            for y in range(num_tiles):
                left = x * tile_size
                upper = y * tile_size
                right = min((x + 1) * tile_size, scaled_width)
                lower = min((y + 1) * tile_size, scaled_height)

                # Пропускаем пустые тайлы
                if left >= right or upper >= lower:
                    print(f"Skipping invalid tile: zoom={zoom}, x={x}, y={y}, "
                          f"left={left}, upper={upper}, right={right}, lower={lower}")
                    continue

                tile = scaled_img.crop((left, upper, right, lower))

                x_folder = os.path.join(zoom_folder, str(x))
                os.makedirs(x_folder, exist_ok=True)
                tile_path = os.path.join(x_folder, f'{y}.jpg')
                tile.save(tile_path, 'JPEG', quality=90)

# Получаем путь к изображению через интерфейс
image_path = get_image_path()
if image_path:
    # Папка, куда будут сохраняться тайлы
    output_folder = filedialog.askdirectory(title='Select folder to save tiles')
    if output_folder:
        generate_tiles(image_path, output_folder)