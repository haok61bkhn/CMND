from id.id import ID
from str.str import STR
from date.date import DATE
from vocr import VOCR
class OCR:
    def __init__(self):
        self.id = ID()
        self.str = STR()
        self.vietocr = VOCR()
        self.date=DATE()
    def taken(self,elem):
     return elem['center'][1]
    
    def taken1(self,elem):
     return elem['center'][0]
    
    def Sort(self,res):
      res.sort(key=self.taken)
      dong1=[]
      try:
        dong1.append(res[0])
      except:
        dong1=[]
      dong2=[]
      for i in range(1,len(res)):
        height=res[i-1]['height']
       # print(height)
       # print(res[i]['center'][1]-res[i-1]['center'][1])
        if( (height/3)<res[i]['center'][1]-res[i-1]['center'][1]):
          dong2.append(res[i])
          for j in range(i+1,len(res)):
            dong2.append(res[j])
          break
        else: dong1.append(res[i])
      #if(dong2==[] and len(dong1)>0) :dong1.append(res[-1])
      dong1.sort(key=self.taken1)
      dong2.sort(key=self.taken1)
      result=[]
      #print("dong 1 : ",len(dong1))
      for x in dong1:
          result.append(x)
      for x in dong2:
          result.append(x)
      return result

    def predict(self,ims,boxes,mode):
         try:
            #print(mode)
            if(mode=="id") : return self.vietocr.recognize(ims[0])
            if(mode=="date"): space="-"
            else: space=" "
            if(len(ims)>0):
                res=[]
                for box,img in zip(boxes,ims):
                    res.append({'center':(int((box[0]+box[2])/2),(box[1]+box[3])/2),'image':img,'height':box[3]-box[1]})
                    #print("y : ", (box[1]+box[3])/2)
                result=self.Sort(res)
                texts=""
                for x in result:
                    im=x['image']
                    if(mode=="name"):
                       texts+=self.vietocr.recognize(im)+space
                    else:
                       texts+=self.vietocr.recognize(im)+space

                return texts[:-1]
            else:
                return ""
         except:
               return ""
if __name__ == "__main__":
    X=OCR()
