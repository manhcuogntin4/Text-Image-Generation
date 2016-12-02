import cv2
import numpy as np
from matplotlib import pyplot as plt
import pyclstm
from PIL import Image
import sys, getopt
def convertImageBinaire(imgPath,isLieu, cropX=0, cropY=0, cropWidth=0, cropHeight=0):
	img = cv2.imread(imgPath,1)
	#img = cv2.bilateralFilter(img,9,75,75)
	if (img.shape>=3):
		img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, imgBinary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	height = np.size(img, 0)
	width = np.size(img, 1)
	height=60
	r,c=img.shape[:2]
	res = cv2.resize(imgBinary,((int)(height*c)/r, height), interpolation = cv2.INTER_CUBIC)
	res=cv2.fastNlMeansDenoising(res,20, 7, 21)
	w=(int)(height*c)/r
	h=height
	res=res[cropY:h-cropHeight, cropX:w-cropWidth] # Crop from x, y, w, h -> 100, 200, 300, 400
	outPath="out.png"
	cv2.imwrite(outPath,res)
	return outPath
def extractText(imgPath,modelPath):
	ocr = pyclstm.ClstmOcr()
	ocr.load(modelPath)
	imgFile = Image.open("out.png")
	text = ocr.recognize(imgFile)
	t=ocr.recognize_chars(imgFile)
	pro=1
	for i in t:
		pro=pro*i.confidence
	#print pro
	text.encode('utf-8')
	f = open('out.txt', 'w')
	f.write(text.encode('utf-8'))
	#print(text.encode('utf-8'))
	return text, pro
def resizeImageColor(imgPath):
	img = cv2.imread(imgPath,1)
	height=100
	r,c=img.shape[:2]
	res = cv2.resize(img,((int)(height*c)/r, height), interpolation = cv2.INTER_CUBIC)
	outPath="out.png"	
	cv2.imwrite(outPath,res)
	return outPath

def eraseContour(img, y, x, h, w):
	xPos=x
	yPos=y
	while xPos <= x+w: #Loop through rows
		while yPos <= y+h:
			img.itemset((yPos, xPos, 0), 255) 
			img.itemset((yPos, xPos, 1), 255)
			img.itemset((yPos, xPos, 2), 255)  
			yPos = yPos + 1
		yPos = y
		xPos = xPos + 1 #Increment X position by 1	


def cleanImage(imgPath):
	image = cv2.imread(imgPath, 1)
	if image.shape[2]>1:
		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
	_,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV) # threshold
	kernel = cv2.getStructuringElement(cv2.MORPH_OPEN,(3,3))
	dilated = cv2.dilate(thresh,kernel,iterations = 2) # dilate
	_,contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
	height, width, channels = image.shape
	for contour in contours:
	# get rectangle bounding contour
		area = cv2.contourArea(contour)
		[x,y,w,h]=cv2.boundingRect(contour)   
		#if ((area < 400 and ( y< 0.2*height)) or (area < 400 and ( y> 0.8*height))):
		if ((h < height/4 and ( y< 0.3*height)) or (h < height/4 and ( y> 0.7*height))):
			eraseContour(image,y,x,h,w)
	outPath='out.png'	
	cv2.imwrite(outPath, image)
	return outPath

total = len(sys.argv)
#modelPath="model-axa-aws.clstm"
modelPath="model-nomprenom2911-binary.clstm"
#modelPath="model-nom-prenom-3011-binary.clstm"
isLieu=0
for i in xrange(total):
	if (i ==1):
		if (sys.argv[i]=="lieu"):
			modelPath="model-lieu2911-binary.clstm"
			isLieu=1
imgPath="158.bin.png"
maxPro=0
textResult=""
path= convertImageBinaire(imgPath, isLieu)
path= cleanImage(path)
text,prof=extractText(path,modelPath)
print text, prof
for i in range (0,3):
	for j in range (0,3):
		for k in range (0,3):
			for h in range (0, 3):
				path= convertImageBinaire(imgPath, isLieu, i,j,k,h)
				#path= cleanImage(path)
				text, pro= extractText(path,modelPath)
				#print text, pro
				if(pro>maxPro):
					maxPro=pro
					textResult=text
print textResult
print maxPro


