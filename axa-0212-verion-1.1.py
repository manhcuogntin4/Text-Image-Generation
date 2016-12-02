import cv2
import numpy as np
from matplotlib import pyplot as plt
import pyclstm
from PIL import Image
import sys, getopt
def convertImageBinaire(imgPath):
	img = cv2.imread(imgPath,1)
	if (img.shape>=3):
		img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, imgBinary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	height = np.size(img, 0)
	width = np.size(img, 1)
	height=60
	r,c=img.shape[:2]
	res = cv2.resize(imgBinary,((int)(height*c)/r, height), interpolation = cv2.INTER_CUBIC)
	res=cv2.fastNlMeansDenoising(res,20, 7, 21)
	outPath="out.png"
	cv2.imwrite(outPath,res)
	return outPath,res

def cropImage(imgFile,cropX=0, cropY=0, cropWidth=0, cropHeight=0):
	h = np.size(imgFile, 0)
	w = np.size(imgFile, 1)	
	res=imgFile[cropY:h-cropHeight, cropX:w-cropWidth]
	outPath="out.png"
	cv2.imwrite(outPath,res)
	return outPath

def extractText(ocr,imgPath):
	imgFile = Image.open(imgPath)
	text = ocr.recognize(imgFile)
	chars=ocr.recognize_chars(imgFile)
	pro=1
	for i in chars:
		pro=pro*i.confidence
	text.encode('utf-8')
	return text, pro

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
imgPath="lieu1.png"
ocr = pyclstm.ClstmOcr()
ocr.load(modelPath)
path,image=convertImageBinaire(imgPath)
text,prof=extractText(ocr,path)
maxPro=0
textResult=""
print text, prof
for i in range (0,3):
	for j in range (0,3):
		for k in range (0,3):
			for h in range (0, 3):
				img= cropImage(image, i,j,k,h)
				#path= cleanImage(path)
				text, pro= extractText(ocr,img)
				if(pro>maxPro):
					maxPro=pro
					textResult=text

print textResult
print maxPro


