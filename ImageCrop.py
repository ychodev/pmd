# 이미지를 배경을 잘라내고 줄여주는 프로그램
# Written by Yongjoo Cho
# Last modified 2/17/2026

import os
from PIL import Image, ImageChops, ImageOps
import sys

def remove_title(im, target_color, background_color):
    img = im.convert("RGB")
    pixels = img.load()

    # 지우고 싶은 글씨 색 (예: 빨강)
    tolerance = 40

    # 픽셀 단위로 검사
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if abs(r - target_color[0]) < tolerance and \
               abs(g - target_color[1]) < tolerance and \
               abs(b - target_color[2]) < tolerance:
                pixels[x, y] = background_color
    return img

def trim(im):
    # 배경색 기준으로 여백 제거
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

if len(sys.argv) < 3:
    print("Usage: python ImageCrop.py original_dir new_dir")
    exit()
else:
    input_dir = sys.argv[1]   # 이미지가 있는 디렉토리
    output_dir = sys.argv[2]  # 결과 저장 디렉토리
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(input_dir, filename)
            img = Image.open(path)
#            img = remove_title(img, (40, 122, 95), (255, 255, 255))
            trimmed = trim(img)
            # crop된 이미지에 3픽셀 여백 추가 
            # 여백 크기 (픽셀 단위)
            # 여백 색상 (예: "white", "black", (R,G,B)) 
            bordered = ImageOps.expand(trimmed, border = 20, fill = "white")
            bordered.save(os.path.join(output_dir, filename))

