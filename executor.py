import time 
import pyautogui
import random

pyautogui.FAILSAFE = True
click_delay = 0.15

class MoveExecutor:
    def __init__(self):
        self.top_left = None
        self.bottom_right = None
        self.flipped = False

    def set_board(self,top_left,bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
    
    def flip(self):
        self.flipped = not self.flipped
    
    def move(self, source, destination):
        if self.bottom_right is None or self.top_left is None:
            raise RuntimeError("Board is not calliberated properly")
        src_pixel = self.square_to_pixel(source)
        dst_pixel = self.square_to_pixel(destination)
        self.click(src_pixel)
        time.sleep(random.randint(1,2))
        self.click(dst_pixel)


    def click(self, position):
        x,y = position
        pyautogui.moveTo(x,y, duration=0.2)
        pyautogui.click()

    # colums: a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7
    # rows: 1=0, 2=1, 3=2, 4=3, 5=4, 6=5, 7=6, 8=7

    def square_to_pixel(self, square): #asci of  a is 97 asci of e is 101  
        column_index = ord(square[0]) - ord('a')
        row_index = int(square[1]) - 1

        bx1,by1 = self.top_left
        bx2,by2 = self.bottom_right
        square_w = (bx2 - bx1) / 8
        square_h = (by2 - by1) / 8

        if not self.flipped:
            col = column_index
            row = 7 - row_index
        else:
            col = 7 - column_index
            row = row_index
        
        px = int(bx1 + col * square_w + square_w/2)
        py = int(by1 + row * square_h + square_h/2)

        return (px,py)

    def preview_squares(self):
        print("all square positions are as follows")
        for i in reversed("12345678"):
            row = ""
            for j in "abcdefgh":
                px,py = self.square_to_pixel(j+i)
                row += f"{j}{i}:{px},{py}"
            print(row)
        print()