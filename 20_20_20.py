from screen_brightness_control import set_brightness, get_brightness
import psutil
import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import sys

def reduce_brightness(current_brightness_screen):
    try:
        # Reducing brightness level (in %)
        set_brightness(0)

        # setting time for which to keep display off (in seconds)
        time.sleep(40)

        # Restore previous brightness level
        set_brightness(float(current_brightness_screen[0]))
    except Exception as e:
        print(f"Error: {e}")

def working_time_timer(time_sec):
    # reading current timer
    start_time = time.time()
    cur_time = 0
    while cur_time<time_sec:
        cur_time = int(time.time()-start_time)
        # Convert elapsed time to minutes and seconds
        cur_time_min = cur_time // 60
        cur_time_sec = cur_time % 60
        
        # Print timer
        print(f"Timer: {cur_time_min:02d}:{cur_time_sec:02d}", end='\r')
        time.sleep(0.1)

def main():
    current_process = {proc.pid for proc in psutil.process_iter()}
    # Choosing time interval for keeping the screen brightness on
    # screen_time = float(input("Please enter your Screen Time for one go \nRecommended time is 20\n")) 
    screen_time = simpledialog.askfloat("Input","Enter Screen Light on time:")

    try:
        count = 0
        while True:
            count += 1
            if count ==30:
                try:
                    # taking user input for continuing or exiting
                    enter_exit = int(input("Press 1 to exit, else 0: "))
            #         enter_exit = messagebox.askquestion("Input", "Do you want to continue?", icon='info', **{"type": "yesno"})
                    if enter_exit == 1:
                        sys.exit()
                    count = 0
                except:
                    count = 0

            # function to show timer
            working_time_timer(screen_time*60)

            # Reading current brightness
            current_brightness_screen = get_brightness()

            # asking to off display or not
            new_proc = {proc.pid for proc in psutil.process_iter()}
            if (new_proc - current_process):
                priority = simpledialog.askfloat("Input","If you want to avoid to off display, press 1 else 0:")
                if(priority == 1):
                    print("High priority process is running")
                    working_time_timer(20*60)
                    time.sleep(20*60)
                    current_process = new_proc
                    
            # calling function to set the display brightness to 0 and back
            reduce_brightness(current_brightness_screen)
            current_process = {proc.pid for proc in psutil.process_iter()}

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
