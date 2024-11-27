import os
import re
import time
from tqdm import tqdm
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
# poetry run img2pdfpy -i "/Users/hahazexiahahazexia/Downloads/租借女友(32)" -p "none" -c "many"
def images_to_pdf(img_folder, pdf_filename):
    output_name = pdf_filename
    if pdf_filename == 'none':
        output_name = "{}.pdf".format(os.path.basename(img_folder))

    print("output_name is {}".format(output_name))

    # 获取文件夹中的所有图片文件
    images = [f for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    # 按照文件名的数字顺序排序
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # 创建 PDF 文件
    c = canvas.Canvas(output_name, pagesize=letter)
    width, height = letter

    for img in tqdm(images, desc="Processing Images {}".format(os.path.basename(output_name)), unit="image"):
        img_path = os.path.join(img_folder, img)
        image = ImageReader(img_path)
        img_width, img_height = image.getSize()

        # 计算缩放比例
        scale = min(width / img_width, height / img_height)
        new_width = img_width * scale
        new_height = img_height * scale

        # 计算居中位置
        x = (width - new_width) / 2
        y = (height - new_height) / 2

        # 绘制图片
        c.drawImage(image, x, y, new_width, new_height)
        c.showPage()  # 添加新的一页

    c.save()  # 保存 PDF 文件

def extract_number(folder_name):
    # 提取文件夹名中的数字，返回第一个找到的数字，若无数字则返回无穷大
    numbers = re.findall(r'\d+', folder_name)
    return int(numbers[0]) if numbers else float('inf')  # 如果没有数字，返回无穷大以排在最后

def get_first_level_folders(img_folder):
    # 确保提供的路径是一个有效的目录
    if not os.path.isdir(img_folder):
        raise ValueError(f"{img_folder} is not a valid folder.")

    # 获取一级文件夹的路径和文件夹名
    first_level_folders = []
    for entry in os.listdir(img_folder):
        full_path = os.path.join(img_folder, entry)
        if os.path.isdir(full_path):  # 检查是否是文件夹
            first_level_folders.append((full_path, entry))

    first_level_folders.sort(key=lambda x: extract_number(x[1]))

    return first_level_folders

def main():
    parser = argparse.ArgumentParser(description='Convert images to a PDF file.')
    parser.add_argument('--img_folder', '-i', type=str, help='Path to the folder containing images.')
    parser.add_argument('--pdf_filename', '-p', type=str, default="none", help='Output PDF file name.')
    parser.add_argument('--convert_type', '-c', type=str, default='one',help='Source file type. one many')

    args = parser.parse_args()
    img_folder = args.img_folder
    pdf_filename = args.pdf_filename
    convert_type = args.convert_type

    if convert_type == 'one':
        images_to_pdf(args.img_folder, args.pdf_filename)
    else:
        folders = get_first_level_folders(img_folder)
        for path, name in folders:
            os.makedirs("{}_pdf".format(img_folder), exist_ok=True)
            output_path = "{}_pdf/{}.pdf".format(img_folder, name)
            images_to_pdf(path, output_path)

if __name__ == '__main__':
    main()
