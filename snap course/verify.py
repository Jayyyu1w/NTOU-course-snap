import ddddocr

def vercode(img):
    ocr = ddddocr.DdddOcr()
    strlist = list(ocr.classification(img))
    strlist = [x.upper() for x in strlist]
    str = "".join(strlist)
    return str