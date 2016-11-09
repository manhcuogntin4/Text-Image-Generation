from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha

#audio = AudioCaptcha(voicedir='/home/cuong-nguyen/2016/Workspace/brexia/Novembre/CodeSources/captcha/captcha/data')
image = ImageCaptcha(fonts=['/home/cuong-nguyen/2016/Workspace/brexia/Novembre/CodeSources/captcha1/captcha/data/COMMUNIS.ttf'])

#data = audio.generate('1234')
#audio.write('1234', 'out.wav')
f = open('test.txt', 'r')
i=0
for line in f:
 i=i+1
 image.write(line, str(i)+".bin.png")
 f1=open(str(i)+".gt.txt",'w')
 f1.write(line)
f.close()

