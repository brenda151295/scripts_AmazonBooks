from PIL import Image 
from os import listdir
path = '/home/ademir/Documents/images/'
files_images = listdir(path)

for image in files_images:
	Image.open(path+image).convert('RGB').save(path+image)
