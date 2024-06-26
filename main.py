import cv2
import mediapipe as mp
import time
import ctypes
import pyautogui as pt
import os
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from PIL import ImageGrab

video = cv2.VideoCapture(0)
mp_cizim = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


yukseklik_esik = 0.5 #0.5'ten buyukse parmak olarak kabul edilir


windows = pt.getAllTitles()

def Kilit():
    ctypes.windll.user32.LockWorkStation()

def Windows():
    for window in windows:
        if window != "Masaüstü":  
            pt.getWindowsWithTitle(window)[0].minimize()  # Pencereyi minimize et
            #time.sleep(0.5)

def fotograf():
    pt.press('win')
    pt.write('Kamera')
    pt.press('enter')
    video.release()
    
    time.sleep(5)
    pt.press('enter')

#tanımladığım favori uygulamayı açmak için oluşturdum
def favUygulama():
    uygulama = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    os.startfile(uygulama)

def githubSayfam():
    url = "https://www.linkedin.com/in/uludag-emre/"
    webbrowser.open(url)


with mp_hands.Hands(static_image_mode=False) as  hands:
    while True:
        kontrol, kamera = video.read()

        rgb = cv2.cvtColor(kamera, cv2.COLOR_BGR2RGB)
        sonuc = hands.process(rgb)
        yedekParmakSayisi = None

        # parmak index atama kısmı
        if sonuc.multi_hand_landmarks:
            for hand_landmarks in sonuc.multi_hand_landmarks:
                yukseklikler = [landmark.y for landmark in hand_landmarks.landmark] #normalleştirilmiş yukseklik listesi                
                
                parmakSayisi = sum(y > yukseklik_esik for y in yukseklikler)
                
                print("parmak sayisi", parmakSayisi)                

                mp_cizim.draw_landmarks(kamera, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                
            yedekParmakSayisi = parmakSayisi

        komut1 = 18     
        komut2 = 15
        komut3 = 12
        komut4 = 10
        komut5 = 9

        
        #time.sleep(2)
        if(yedekParmakSayisi == komut1):
            Kilit()
            break
        elif(yedekParmakSayisi == komut2):
            Windows()
            break
        elif(yedekParmakSayisi == komut3):
            favUygulama()
            break
        elif(yedekParmakSayisi == komut4):
            fotograf()            
            break
        elif(yedekParmakSayisi == komut5):
            githubSayfam()
            break



        cv2.imshow('El Cizimi',kamera)        

        if cv2.waitKey(10) == 27:
            break

video.release()
cv2.destroyAllWindows()
