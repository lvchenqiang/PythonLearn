from PIL import Image
from  PIL import  ImageChops
from PIL import ImageDraw
"""
 Image模块提供了一个相同名称的类，即image类，用于表示PIL图像。这个模块还提供了一些函数，包括从文件中加载图像和创建新的图像。

 Image模块是PIL中最重要的模块，它提供了诸多图像操作的功能，比如创建、打开、显示、保存图像等功能，合成、裁剪、滤波等功能，
  获取图像属性功能，如图像直方图、通道数等。
 
 """
im = Image.open("index.png")
# 图片的像素模式  RGBA
print(im.mode)
# ('R', 'G', 'B', 'A')
print(im.getbands())
# 显示图片
# im.show()


"""
  ImageChops模块包含一些算术图形操作，叫做channel operations（“chops”）。
  这些操作可用于诸多目的，比如图像特效，图像组合，算法绘图等等。通道操作只用于8位图像（比如“L”模式和“RGB”模式）。
 """
# 复制图片
im_dup = ImageChops.duplicate(im)
# im_dup.show()
# 获取差值图片  由于两张图片一致 差值图片空白
im_diff = ImageChops.difference(im, im_dup)
im_diff.show()






