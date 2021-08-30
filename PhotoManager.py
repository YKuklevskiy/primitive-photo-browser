from tkinter import *
import tkinter.filedialog as fileDialog
from PIL import ImageTk, Image, UnidentifiedImageError
import os


class PhotoManager:
    def __init__(self, window: Tk, canvas: Canvas):
        self.current_photos = None
        self.current_index = 0
        self.current_dir = None
        self.window = window
        self.canvas = canvas
        self._displayed_image = None
        self._image_instance = None

    def choose_photos(self, mode: str):
        if mode == 'dir': # choose directory
            self.current_dir = fileDialog.askdirectory(initialdir='/', title='Select directory...')
            self.current_photos = [file for file in os.scandir(self.current_dir) if file.is_file()]
            for file in self.current_photos:
                print(file)
        else: # choose a photo
            temp = fileDialog.askopenfile(mode='r', initialdir='/', title='Select photo...').name
            file_name = temp.split('/')[-1]
            self.current_dir = os.path.dirname(temp)
            self.current_photos = [file for file in os.scandir(self.current_dir) if file.is_file()]
            for i in range(len(self.current_photos)):
                if(self.current_photos[i].name == file_name):
                    self.current_index = i
                    break
        
        print(self.current_photos[self.current_index].path)
        self.update_canvas()
    

    def delete_current_photo(self):
        pass


    def update_canvas(self):
        try: # try to open file as image
            img = Image.open(self.current_photos[self.current_index].path)
        except UnidentifiedImageError: # display error message
            print('App could not open the image.')
            return

        # todo display a message while image is loading, check if an image is currently loading

        w2h = float(img.width)/img.height # width to height ratio
        canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
        if canvas_size[0]/canvas_size[1] > w2h:
            img = img.resize((int(canvas_size[1]*w2h), canvas_size[1]), Image.ANTIALIAS)
        else:
            img = img.resize((canvas_size[0], int(canvas_size[0]/w2h)), Image.ANTIALIAS)
        self._displayed_image = ImageTk.PhotoImage(img)
        img_inst = self.canvas.create_image(canvas_size[0]/2, canvas_size[1]/2, image=self._displayed_image)
