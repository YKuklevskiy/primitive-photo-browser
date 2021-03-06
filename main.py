from tkinter import *
from win32api import GetMonitorInfo, MonitorFromPoint
from PhotoManager import PhotoManager
from send2trash import send2trash


'''

Project uses pywin32 and send2trash modules.

'''


window = Tk()
window.title("Photo Browser")
# window.attributes('-fullscreen', True)
# basically gets work area of a monitor (without TaskBar)
monitor_work_area = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
# window is resizable, but initially its a little smaller than screen size
window.geometry(f'{monitor_work_area[2] - 40}x{monitor_work_area[3] - 40}+0+0')

#while debugging
window.geometry(f'{monitor_work_area[2] - 400}x{monitor_work_area[3] - 400}+0+0')

window.resizable(False, False)

photo_switch_state = [False, False] # left arrow, right arrow: pressed or not


# called on any key pressed
def key_pressed(event):
    if event.keysym == 'Left':
        if not (photo_switch_state[0] or photo_switch_state[1]):
            manager.switch_photo('Previous')
        photo_switch_state[0] = True
    elif event.keysym == 'Right':
        if not (photo_switch_state[0] or photo_switch_state[1]):
            manager.switch_photo('Next')
        photo_switch_state[1] = True


# called on any key stopped being pressed
def key_released(event):
    if event.keysym == 'Left':
        photo_switch_state[0] = False
    elif event.keysym == 'Right':
        photo_switch_state[1] = False


window.bind('<Key>', key_pressed)
window.bind('<KeyRelease>', key_released)

# button handlers
def choose_dir():
    manager.choose_photos('dir')


def choose_photo():
    manager.choose_photos('photo')


def delete_photo():
    manager.delete_current_photo()


def rotate_anticlockwise():
    pass


def rotate_clockwise():
    pass


# buttons
# button frame consists of two frames each stuck to sides of the window
buttons_frame = Frame(window)
left_frame = Frame(buttons_frame)
right_frame = Frame(buttons_frame)

choose_dir_button = Button(left_frame, text='Choose directory...', relief='groove', 
                           font=('Lato', 14), command=choose_dir)
choose_photo_button = Button(left_frame, text='Choose photo...', relief='groove', 
                             font=('Lato', 14), command=choose_photo)
delete_button = Button(left_frame, text='Delete photo', bg='red', fg='white', font=('Lato', 14),
                       relief='raised', activebackground='red', command=delete_photo)
choose_dir_button.grid(column=0, row=0)
choose_photo_button.grid(column=1, row=0)
delete_button.grid(column=2, row=0)

aclockwise_rotate_button = Button(right_frame, text = 'left_r', image=None, command=rotate_anticlockwise)
clockwise_rotate_button = Button(right_frame, text = 'right_r', image=None, command=rotate_clockwise)
aclockwise_rotate_button.grid(column=0, row=0)
clockwise_rotate_button.grid(column=1, row=0)
left_frame.pack(fill=X, side=LEFT)
right_frame.pack(fill=X, side=RIGHT)
buttons_frame.pack(fill=X)


# canvas
canvas = Canvas(window, highlightbackground="black", highlightthickness=1)
canvas.configure(width=window.winfo_width(),
                 height=window.winfo_height() - buttons_frame.winfo_height())
canvas.pack(fill='both', expand=True)

manager = PhotoManager(window, canvas)

window.mainloop()
