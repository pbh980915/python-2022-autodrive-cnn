# 사용할 코드들을 설정합니다.

print("tensorflow import start ")
from app_train import *
print("tensorflow import complete ")

import pygame
import sys
import serial
import pyautogui as pag
import time
import cv2


    




# pygame 출력용 이미지 처리 함수입니다.
def load_image(path, scale = None, rotate = None):
    img = pygame.image.load(path)
    if scale  != None : img = pygame.transform.scale ( img, scale )
    if rotate != None : img = pygame.transform.rotate( img, rotate )
    return img

def update_image(img, scale = None, rotate = None):
    if scale  != None : img = pygame.transform.scale ( img, scale )     
    if rotate != None : img = pygame.transform.rotate( img, rotate )
    return img

def display_image(screen, img, location):
    return screen.blit( img, location ) 





class App:
    
    # 1. 앱이 설정되고 실행합니다.
    def __init__    (self): 
        self.set_app() 
        self.set_prof()
        self.run()
        
    # 2. 앱이 실행되는 부분입니다.    
    def run (self):
        while self.running==True:
            t = time.time()
            self.control()
            self.update()
            print(time.time()-t)
            self.display()
            
            
            
            
    # 창을 설정하는 부분입니다.        
    def set_app (self): 
        pygame.init()
        pygame.display.set_caption("pygame form1")		
        self.screen = pygame.display.set_mode((640, 350))	
        self.clock = pygame.time.Clock()	
        self.font  = pygame.font.SysFont( "arial", 27, True, False)
        self.running = True    
        
        
        
        
    # 프로그램의 내부 기능을 설정하는 부분입니다.    
    def set_prof (self): 
        self.keyboard = [0,0,0,0,0,0] # up, down, right, left, shift ctrl
        self.isBreak  = 0         # shift
        self.throttle = 0         # drive speed
        self.motorRL  = [0,0]
        self.ard = serial.Serial(port='COM13', baudrate=115200)
        self.train = None
        
        self.mode = "NULL"
        print("model load start")
        self.model = None
        self.tflite_model = None
        try:
            self.model = tf.keras.models.load_model("aiModel.h5")
            self.tflite_model = tf.lite.Interpreter("aiModel_lite.tflite")
        except: pass
        print("model load complete")
        
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.rscam = None
        self.npcam = None
        self.sufcam = None
        
    
    
            
    # 2-1. 조작이 일어나는 부분입니다.        
    def control (self): 
        for event in pygame.event.get():			
            if event.type == pygame.QUIT: self.running = False;	sys.exit()	
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()
                # 버튼 조작입니다.
                if (10 < pos[0] < 260)&(180 < pos[1] < 220): 
                    if self.mode == "NULL": self.mode = "RECORD"
                    else: self.mode = "NULL"
                if (10 < pos[0] < 260)&(230 < pos[1] < 270):
                    if self.mode == "NULL": self.mode = "TRAIN"
                    else: self.mode = "NULL"
                if (10 < pos[0] < 260)&(280 < pos[1] < 320):
                    if self.mode == "NULL": self.mode = "AUTO"
                    else: self.mode = "NULL"
                
            if event.type == pygame.MOUSEBUTTONUP: pass
            if event.type == pygame.MOUSEMOTION: pass
                
            if event.type == pygame.KEYDOWN: 
                # 키보드 조작입니다.
                if event.key == pygame.K_UP:    self.keyboard[0] = 1
                if event.key == pygame.K_DOWN:  self.keyboard[1] = 1
                if event.key == pygame.K_RIGHT: self.keyboard[2] = 1
                if event.key == pygame.K_LEFT:  self.keyboard[3] = 1
                if event.key == pygame.K_LSHIFT: self.keyboard[4] = 1
                if event.key == pygame.K_LCTRL: self.keyboard[5] = 1
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_UP:    self.keyboard[0] = 0
                if event.key == pygame.K_DOWN:  self.keyboard[1] = 0
                if event.key == pygame.K_RIGHT: self.keyboard[2] = 0
                if event.key == pygame.K_LEFT:  self.keyboard[3] = 0
                if event.key == pygame.K_LSHIFT: self.keyboard[4] = 0
                if event.key == pygame.K_LCTRL: self.keyboard[5] = 0
                
                	
                 
                 
                 	
                  	
    # 2-2. 갱신이 일어나는 부분입니다.    
    def update (self): 
        # get cam
        ret, frame = self.cap.read()
        self.npcam = np.array(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        self.sufcam = pygame.pixelcopy.make_surface(np.rot90(self.npcam))
                
        # throttle update
        if self.keyboard[4] == 1: self.throttle += 5 #shift
        if self.keyboard[5] == 1: self.throttle = int(self.throttle/4*3)#ctrl
        
        # throttle limit
        if self.throttle < -255  : self.throttle = -255
        if self.throttle >  255  : self.throttle =  255
        
        # order actuator
        self.motorRL = [2,2]
        if self.keyboard[0] == 1: self.motorRL = [1,1] #L후진 R전진
        if self.keyboard[1] == 1: self.motorRL = [0,0] #L전진 R후진
        if self.keyboard[2] == 1: self.motorRL = [1,0] #L후진 R전진
        if self.keyboard[3] == 1: self.motorRL = [0,1] #L전진 R후진
        
        
            
        # mode recording
        self.update_recoding()
        
        # mode auto drive  
        self.update_autodrive()


        if self.mode == "AUTO":
            if self.motorRL[0] != self.motorRL[1]:
                self.ard.write([101, 250, self.motorRL[0], self.motorRL[1]])
            else:
                if self.motorRL[0] == 2: self.motorRL = [1,1]
                self.ard.write([101, 200, self.motorRL[0], self.motorRL[1]])
            #time.sleep(0.3)
            #self.ard.write([101, 0, self.motorRL[0], self.motorRL[1]])
            #self.ard.write([101, 0, self.motorRL[0], self.motorRL[1]])
            
        else:
            if self.keyboard[2] | self.keyboard[3]:
                self.ard.write([101, abs(self.throttle)+50, self.motorRL[0], self.motorRL[1]])
            else:
                self.ard.write([101, abs(self.throttle), self.motorRL[0], self.motorRL[1]])

            


    
    
    
    
    # 학습을 위한 이미지를 촬영하는 모드입니다.
    def update_recoding (self): 
        if self.mode == "RECORD":
            
            s = str(self.throttle) 
            t = str(int(time.time()*10)) #10fps #overwrite
            d = str(self.motorRL[0])+str(self.motorRL[1])
            path = "records/t"+t+"s"+s+"d"+d+".png"
            
            # code of camera
            if self.sufcam != None:
                if self.motorRL[0] != 2:
                    self.sufcam = update_image(self.sufcam, scale = (160,150))
                    pygame.image.save(self.sufcam,path)
            # 스크린샷으로 이미지 샘플을 얻는 테스트 코드입니다. 
            #pag.screenshot(path, region=(0, 50, 500, 200))
            #sys.exit()
        



    
    
    
    # 학습된 데이터로 주행을 하는 모드입니다.
    def update_autodrive(self):
        if self.mode == "AUTO":
            if self.model == None:
                print("모델이 없습니다.")
                return

           #이미지를 읽어옵니다.
            #img = pygame.surfarray.pixels3d(self.aicam)
            img = Image.fromarray(self.npcam).resize((56, 28))
            
            img = np.asarray(img).astype(float)/255
            img = np.vstack((img[:,:,0],img[:,:,1],img[:,:,2]))

            predict = np.round(self.model(np.array([img])))
            
            motorRL = np.argmax(predict, axis=1)[0]%5
            throttle = np.argmax(predict, axis=1)[0]//5

            
            if motorRL == 1: self.motorRL = [1,0];
            if motorRL == 2: self.motorRL = [0,1];
            if motorRL == 3: self.motorRL = [1,1]; 
            self.throttle = throttle*50
            pass
    



    
    
    
    # 촬영된 학습 데이터로 신경망을 형성합니다.
    def update_training(self):
        if self.mode == "TRAIN":
            # app_train을 실행합니다.
            print("training func")
            self.model = train()
            print("training complete")
            self.model.save('aiModel.h5')
            converter = tf.lite.TFLiteConverter.from_saved_model('aiModel.h5')
            tflite_model = converter.convert()
            with open('aiModelLite.tflite', 'wb') as f:
              f.write(tflite_model)
            print("convert model 2 tflite complete")
            self.mode = "NULL"

            self.tflite_model = tflite_model
    
        
        
        
        
        
        
    # 2-3. 출력이 일어나는 부분입니다. GUI를 꾸밉니다.
    def display (self): 
        self.screen.fill((0,0,0))	
        
        text_mode = self.font.render("mode : "+str(self.mode), True, (255,255,255))
        text_throttle = self.font.render("throttle : "+str(self.throttle), True, (255,255,255))
        text_motorRL = self.font.render("motorRL : "+str(self.motorRL), True, (255,255,255))
        
        self.screen.blit(text_mode,(10,10))
        self.screen.blit(text_throttle,(10,50))
        self.screen.blit(text_motorRL,(10,90))
        
        pygame.draw.rect(self.screen, (255,255,255),[300,20,320,300])
        if self.sufcam == None:
            text = self.font.render("CAMERA DISPLAY", True, (0,0,0))
            self.screen.blit(text,(310,30))
        else:
            self.screen.blit(
                update_image(self.sufcam,scale=(320,300)), (300,20))
        
        pygame.draw.line(self.screen, (0,255,0), [460,20], [460,320],2)
        pygame.draw.line(self.screen, (0,255,0), [320,170], [620,170],2)
        pygame.draw.circle(self.screen, (0,255,0), [460,170], 60,2)        
        
        if self.mode == "RECORD":
            pygame.draw.rect(self.screen, (150,50,50), [10,180,250,40])
            text = self.font.render("RECORD OFF", True, (0,0,0))
            self.screen.blit(text,(20,180))
        else:
            pygame.draw.rect(self.screen, (255,255,255), [10,180,250,40])
            text = self.font.render("RECORD ON", True, (0,0,0))
            self.screen.blit(text,(20,180))
            
        
        if self.mode == "TRAIN":
            pygame.draw.rect(self.screen, (150,50,50), [10,230,250,40])
            text = self.font.render("TRAINING...", True, (0,0,0))
            self.screen.blit(text,(20,230))
        else:
            pygame.draw.rect(self.screen, (255,255,255), [10,230,250,40])
            text = self.font.render("TRAIN START", True, (0,0,0))
            self.screen.blit(text,(20,230))
            
        
        if self.mode == "AUTO":
            pygame.draw.rect(self.screen, (150,50,50), [10,280,250,40])
            text = self.font.render("AUTO DRIVE OFF", True, (0,0,0))
            self.screen.blit(text,(20,280))
        else:
            pygame.draw.rect(self.screen, (255,255,255), [10,280,250,40])
            text = self.font.render("AUTO DRIVE ON", True, (0,0,0))
            self.screen.blit(text,(20,280))
            
            
        pygame.display.update()	
        self.clock.tick(120)
        
        if self.mode == "TRAIN":
            self.update_training()
        


if __name__ == "__main__":
    app = App()
