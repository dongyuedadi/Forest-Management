import fitz  # PyMuPDF
import os
from PIL import Image
import io
pdf_path=r'C:\Users\hys5637428\Desktop\20240423物候相2.pdf'
output_dir=r'C:\Users\hys5637428\Desktop'
def pdf_to_jpg(pdf_path, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    image_count = 0
    # 遍历PDF中的每一页
    for page_num in range(len(doc)):
        page = doc[page_num]
        # 获取页面中的图片
        images = page.get_images()
        # 遍历页面中的每一个图片
        for img_num, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # 使用PIL将图片数据转换为JPG格式
            image = Image.open(io.BytesIO(image_bytes))
            output_path = os.path.join(output_dir, f"image_{image_count}.jpg")
            image.save(output_path, "JPEG")
            # 更新图片计数
            image_count += 1
            # 关闭PDF文件
    doc.close()
# 使用函数
pdf_to_jpg(pdf_path, output_dir)