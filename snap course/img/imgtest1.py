import os
import ddddocr
os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    ocr=ddddocr.DdddOcr()
    with open('pic2.jpg','rb') as f:
        image=f.read()
    str=ocr.classification(image)
    print(str)