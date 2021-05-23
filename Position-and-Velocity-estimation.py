import matplotlib.pyplot as plt
import pylab
import cv2
'''
Input: label text files, image
output: pos and velocity estimated image
'''

def label(path):
    bbox_list = []
    # open txt file
    with open(path, "r") as file:
        content = file.readlines()
        # drop '\n'
        content = [i.rstrip('\n') for i in content]
        # label is in xywh format
        # change to pixel coordinates
        for obj in content:
            XYWH = obj.split(' ')
            XYWH = [float(i) for i in XYWH]
            X = XYWH[1] * 1280  # 1280 image w
            Y = XYWH[2] * 720  # 720 image h
            H = XYWH[-1] * 720
            W = XYWH[-2] * 1280
            x1, x2 = int(X - W*0.5), int(X + W*0.5)
            y1, y2 = int(Y - H*0.5), int(Y + H*0.5)
            bbox_list.append([x1, y1, x2, y2])
        return bbox_list
def task1(bot,right):
  height=2.5
  fx =714.1526
  fy = 710.3725
  cx = 713.85
  cy = 327

  distancex=fy*height/abs((bot-cy))
  distancey=distancex *(right-cx)/fx
  return distancex,distancey
img_list=[str(i) for i in range(1,1000)]
countx=0
county=0
for i in img_list:
     Single_path = './runs/detect/exp8/labels/{d}.txt'.format(d=i)
     # convert  label to pixel coordinates
     bbox = label(Single_path)
     Single_path = './runs/detect/exp8/labels/{d}0.txt'.format(d=i)
     bbox2=label(Single_path)
     img=cv2.imread('../train/{d}.jpg'.format(d=i))
     img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     for j in range(len(bbox)):
      bot=bbox[j][3]
      right=bbox[j][2]
      top=bbox[j][1]
      left=bbox[j][0]
      bot2=bbox2[j][3]
      right2=bbox2[j][2]
      x1,y1=task1(bot,right)
      x2,y2=task1(bot2,right2)
      x1=round(x1,2)
      y1=round(y1,2)
      x2=round(x2,2)
      y2=round(y2,2)
      vy=round((y2-y1)/2,2)
      vx=round((x2-x1)/2,2)
      countx=countx+x1
      county=county+y1
      img=cv2.rectangle(img, (left, top), (right, bot), (255, 255, 0), 2)
      img=cv2.putText(img,'velocity:({x},{y})'.format(x=vx,y=vy),(right,top-30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
      img=cv2.putText(img,'position:({x},{y})'.format(x=x1,y=y1),(right,top),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
     cv2.imwrite('../results/' + str(i) + '.jpg', img)
    #  print(bbox) 
     
     plt.imshow(img)  
