import pytesseract
from PIL import Image

# 有利识别的特点 ：
#
# 由纯阿拉伯数字组成
# 字数为4位
# 字符排列有规律
# 字体是用的统一字体
image = Image.open('index.png')
print(image)
text = pytesseract.image_to_string(image)
print(text)