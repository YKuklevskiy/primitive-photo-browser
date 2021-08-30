from tkinter import *
from win32api import GetMonitorInfo, MonitorFromPoint
from PhotoManager import PhotoManager
from send2trash import send2trash

window = Tk()
window.title("Photo Browser")
# window.attributes('-fullscreen', True)
# basically gets work area of a monitor (without TaskBar)
monitor_work_area = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")
# window is resizable, but initially its a little smaller than screen size
window.geometry(f'{monitor_work_area[2] - 40}x{monitor_work_area[3] - 40}+0+0')
window.resizable(False, False)
manager = PhotoManager(window)


def choose_dir():
    manager.choose_photos('dir')


def choose_photo():
    manager.choose_photos('photo')


def delete_photo():
    pass


# buttons
buttons_frame = Frame(window)
choose_dir_button = Button(buttons_frame, text='Choose directory...', relief='groove', command=choose_dir)
choose_photo_button = Button(buttons_frame, text='Choose photo...', relief='groove', command=choose_photo)
delete_button = Button(buttons_frame, text='Delete photo', bg='red', fg='white',
                       relief='raised', activebackground='red', command=delete_photo)
choose_dir_button.grid(column=0, row=0)
choose_photo_button.grid(column=1, row=0)
delete_button.grid(column=2, row=0)
buttons_frame.pack(fill=X)
buttons_frame.update()

# canvas
canvas = Canvas(window)
canvas.configure(width=window.winfo_screenwidth() - 10,
                 height=window.winfo_screenheight() - 80 - buttons_frame.winfo_height())
canvas.pack(fill='both', expand=True)

window.mainloop()
