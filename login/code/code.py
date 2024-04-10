import os

from PIL import Image, ImageDraw, ImageFont
from random import choice, randint


def create_captcha_content():
    # 创建一张图片
    img = Image.new(mode="RGB", size=(110, 40), color=(255, 255, 255))
    # 创建一个画笔
    draw = ImageDraw.Draw(img, mode="RGB")
    font = ImageFont.truetype(r"./ARLRDBD.TTF", size=30)
    # 自定义验证码内容
    text = "ABCDEFG123456789"

    # 存放四位数的验证码
    captcha_text = ""

    for num in range(4):
        captcha_text += choice(text)

    x = 15
    for i in captcha_text:
        # 为每一个验证码设置不同的颜色
        R = str(randint(0, 255))
        G = str(randint(0, 255))
        B = str(randint(0, 255))
        draw.text((x, 3),
                  text=i,
                  font=font,
                  fill=f"rgb({R},{G},{B})"
                  )
        x += 20

    # 添加干扰线条
    for i in range(1, randint(3, 6)):
        x1, y1 = randint(0, 100), randint(0, 30)
        x2, y2 = randint(0, 100), randint(0, 30)
        R = str(randint(0, 255))
        G = str(randint(0, 255))
        B = str(randint(0, 255))
        draw.line((x1, y1, x2, y2), fill=f"rgb({R},{G},{B})", width=2)

    # 添加干扰点
    for i in range(1, randint(30, 60)):
        x1, y1 = randint(0, 100), randint(0, 30)
        R = str(randint(0, 255))
        G = str(randint(0, 255))
        B = str(randint(0, 255))
        draw.point([x1, y1], fill=f"rgb({R},{G},{B})")
    return [img, captcha_text]

#
# # 调用函数获取图像和验证码文本
# captcha_img, captcha_text = create_captcha_content()
#
# # 保存图像到文件
# captcha_img.save("captcha.png")
#
# # 打印验证码文本
# print("验证码文本:", captcha_text)
