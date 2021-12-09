"""
    link: https://github.com/JaviS-Rei/captcha_cas
    input:   original captcha image in CAS 
    output:  answer in type string
    usage:   
        from captcha_recognizer_cas import captha_recognize
        res = captcha_recognize(path)
    
    performance: 1500 captchas per sec
    
    Note:
        1. this program can only recognize captcha image in CAS.
        2. performance optimizing causes little UNREADABLE code.
    
"""

from PIL import Image
import io
import numpy as np
from requests.sessions import Session

from util.log import log

x0_list = [6, 19, 32, 45]
x1_list = [16, 29, 42, 55]
threshold = 125

# set label path
label_dir = r"./cas/label/%d.jpg"
label_set = []
for i in range(10):
    label_set.append((np.array(Image.open(label_dir % i).convert("L"))) < threshold)


def char_cmp(img, label):
    diff = []
    for i in range(10):
        diff.append(np.sum(img ^ label[i]))
    return diff.index(min(diff))


def captcha_recognize(bsio) -> str:
    img = np.array(Image.open(bsio)) < threshold
    res = ""
    for i in range(4):
        x0_ = x0_list[i]
        x1_ = x1_list[i]
        res += str(char_cmp(img[:, x0_:x1_], label_set))
    return res


# 二值化处理 灰度阈值设为125，高于这个值的点全部填白色
def two_value(bsio, threshold=125):
    # 打开文件夹中的图片
    image = Image.open(bsio)

    # 灰度图 模式“L” 每个像素用8个bit表示，0表示黑，255表示白
    # 公式 L = R * 299/1000 + G * 587/1000+ B * 114/1000
    lim = image.convert("L")
    table = []

    for j in range(256):
        if j < threshold:
            # 填黑色
            table.append(0)
        else:
            # 填白色
            table.append(1)
    # 对图像像素操作 模式“1” 为二值图像，非黑即白。但是它每个像素用8个bit表示，0表示黑，255表示白
    bim = lim.point(table, "1")
    imgIO = io.BytesIO()
    bim.save(imgIO, format="JPEG")
    return imgIO


def cas_ocr_url(sess: Session, url: str) -> str:
    resp = sess.get(url)
    bsio = io.BytesIO(resp.content)
    bsio = two_value(bsio)
    res = captcha_recognize(bsio)
    log(f"ocrRes:{res}")
    return res
