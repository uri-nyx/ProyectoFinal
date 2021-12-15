import sys

def readimg(path: str) -> bytes:
    
    with open(path, "rb") as img:
        data = img.read()
    
    return data

def img2text(data: bytes) -> str:
    text = []
    
    for char in data:
        text.append(hex(char))
    
    longS = ""
    i = 0
    for s in text:
        longS += s[2:]
        if i > 40:
            i = 0
            longS += "\n"
        i += 1
        
        
    return longS

def main(argv):
    if len(argv) != 2:
        print("Usage: " + argv[0] + "<path-to-image>")
        return
        
    img_path = argv[1]
    
    print(img2text(readimg(img_path)))
    
if __name__ == "__main__":
    main(sys.argv)