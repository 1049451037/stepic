import stepic
from PIL import Image

img = Image.open('pic.jpg')
data = b'hello'
modified = stepic.encode(img, data)
getdata = stepic.decode(modified)
print(getdata)