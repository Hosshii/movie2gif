# coding: utf-8
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np

# define
video_file = './test.mp4'


cap = cv2.VideoCapture(video_file)
i = 0
images = []
while(cap.isOpened()):
    flag, frame = cap.read()  # 動画を1フレームずつ読み込む
    if not flag:
        break

    image_pil = Image.fromarray(frame)
    resize = image_pil.resize((200, 80), Image.LANCZOS)
    gray_img = resize.convert('L')

    img_dot_array = np.array(gray_img)
    norm_img_array = img_dot_array / 255
    lines = [0]*gray_img.size[1]

    for i in range(0, gray_img.size[1]):
        print(' ')
        for j in range(0, gray_img.size[0]):
            if norm_img_array[i, j] > 0.9:
                print('#', end='')
                lines[i] = '#' if j == 0 else lines[i] + '#'
            elif norm_img_array[i, j] > 0.7:
                print('k', end='')
                lines[i] = 'k' if j == 0 else lines[i] + 'k'
            elif norm_img_array[i, j] > 0.5:
                print('>', end='')
                lines[i] = '>' if j == 0 else lines[i] + '>'
            elif norm_img_array[i, j] > 0.3:
                print('\'', end='')
                lines[i] = '\'' if j == 0 else lines[i] + '\''
            else:
                print(' ', end='')
                lines[i] = ' ' if j == 0 else lines[i] + ' '
    print('\033[H')
    font = ImageFont.truetype(
        "/Users/wistre/Library/Fonts/Ricty-Bold.ttf", 17)
    w, h = max(font.getsize(line) for line in lines)
    img = Image.new("RGB", (w, h*len(lines)), "#000000")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        # print(line)
        draw.text((0, i*h), line, fill="#ffffff")
    images.append(img)

    i += 1

cap.release()
images[0].save('movie2gif.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
