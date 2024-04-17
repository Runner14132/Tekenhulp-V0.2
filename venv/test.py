from PIL import Image, ImageDraw
img = Image.open("monica-lee6.png")
print(img)
draw = ImageDraw.Draw(img)

print (draw)

txt = "Best platform"
draw.line((0, 0, 250, 250), fill =(0, 0, 0), width=10)
# img.save('graph.png')
img.show()