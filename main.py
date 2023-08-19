import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import pygame
import tkinter

textList = []
fontTitle = None
font = None
tk_win = tkinter.Tk()
text = None

def setFont():
    global fontTitle
    fontTitle = ImageFont.truetype('siyuanheiti.otf', 100)
    global font
    font = ImageFont.truetype('siyuanheiti.otf', 40)

def playMusicAsync():
    pygame.mixer.init()
    pygame.mixer.music.load('starwars_bgm.mp3')
    pygame.mixer.music.play(start=0.0)

def stopMusicAsync():
    pygame.mixer.music.stop()

def buildMatrix(h,w):
    k = 0.3
    src = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    dst = np.float32([[w*k, h*0.1], [w*(1-k), h*0.1], [0, h], [w, h]])
    return cv2.getPerspectiveTransform(src, dst)

def setBackgroundAndText():
    global textList,font,fontTitle

    imgBk = cv2.imread("starwars_bg.jpg", cv2.IMREAD_COLOR)
    h,w,_ = imgBk.shape
    matrix = buildMatrix(h,w)
    textPos_y = h
    while cv2.waitKey(20)!=ord('q'):
        textLayer = Image.new("RGB",(w,h))
        draw = ImageDraw.Draw(textLayer)

        for i in range(len(textList)):
            textFont = (font if (i != 0) else fontTitle)
            textWidth,textHeight = textFont.getsize(textList[i])

            textPos_x = (w-textWidth) >> 1
            draw.text((textPos_x,textPos_y+i*(textHeight+8)),textList[i],font=textFont,fill=(255,202,13))
        # OpenCV  透视变换
        im = cv2.cvtColor(np.asarray(textLayer),cv2.COLOR_RGB2BGR)
        imgPerspective = cv2.warpPerspective(im,matrix,(w,h))
        imgAdded = cv2.add(imgPerspective,imgBk)
        cv2.imshow('https://space.bilibili.com/39665558', imgAdded)
        textPos_y -= 1

def onRunBtnClicked(event):
    global textList,text
    textInfo = text.get("1.0", "end")
    textList = textInfo.splitlines()
    setFont()
    playMusicAsync()
    setBackgroundAndText()
    stopMusicAsync()
    cv2.destroyAllWindows()


def createInitWindow():
    global textList,tk_win,text

    tk_win.title('StarWar Text')
    tk_win.geometry('400x160')

    text = tkinter.Text(tk_win,width=55,height=8,undo=True,autoseparators=False)
    text.pack(side='top',anchor='center')

    run_btn = tkinter.Button(tk_win,text='Run',width=8,height=2)
    run_btn.pack(side='top',anchor='center')
    run_btn.bind('<Button-1>',onRunBtnClicked)
    tk_win.mainloop()


if __name__ == '__main__':
    createInitWindow()

