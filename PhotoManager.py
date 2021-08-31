from tkinter import *
import tkinter.filedialog as fileDialog
from PIL import ImageTk, Image, UnidentifiedImageError
import os

# count of images to store in cache
# has to be odd as the image currently loaded will 
# have equal number of next and previous images loaded in cache
CACHE_SIZE = 11 

class PhotoManager:
    def __init__(self, window: Tk, canvas: Canvas):
        self.current_photos = None
        self.current_index = 0
        self.current_dir = None
        self.window = window
        self.canvas = canvas
        self._cached_images = None
        self._current_instance = None

    def choose_photos(self, mode: str):
        if mode == 'dir': # choose directory
            self.current_dir = fileDialog.askdirectory(initialdir='/', title='Select directory...')
            if(self.current_dir == ''): # Cancelled choosing directory
                return
            
            self.current_photos = [file for file in os.scandir(self.current_dir) if file.is_file()]
            for file in self.current_photos:
                print(file)
        else: # choose a photo
            file = fileDialog.askopenfile(mode='r', initialdir='/', title='Select photo...')
            if(file == None): # Cancelled choosing file
                return

            temp = file.name
            file_name = temp.split('/')[-1]
            self.current_dir = os.path.dirname(temp)
            self.current_photos = [file for file in os.scandir(self.current_dir) if file.is_file()]
            for i in range(len(self.current_photos)):
                if(self.current_photos[i].name == file_name):
                    self.current_index = i
                    break
        
        print(self.current_photos[self.current_index].path)
        self.cache_images()
    

    def delete_current_photo(self):
        pass


    def cache_images(self):

        # initializing cache
        cache_size = CACHE_SIZE
        if len(self.current_photos) < CACHE_SIZE:
            cache_size = len(self.current_photos)
        self._cached_images = [None] * cache_size

        for i in range(cache_size):
            try: # try to open file as image
                index = self.current_index+i-(cache_size//2) # current image index in current_photos
                img = Image.open(self.current_photos[index % cache_size].path)
            except UnidentifiedImageError: # display error message
                self._cached_images[i] = 'App could not open the image.'
                continue
            except PermissionError: # display error message
                self._cached_images[i] = 'Permission to open that file denied.'
                continue
        
            #### not here :) #### todo display a message while image is loading, check if an image is currently loading

            # scaling to screen
            w2h = float(img.width)/img.height # width to height ratio
            canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
            if canvas_size[0]/canvas_size[1] > w2h:
                img = img.resize((int(canvas_size[1]*w2h), canvas_size[1]), Image.ANTIALIAS)
            else:
                img = img.resize((canvas_size[0], int(canvas_size[0]/w2h)), Image.ANTIALIAS)
            
            self._cached_images[i] = ImageTk.PhotoImage(img)
            # that is for rendering images
            # self._current_instance = self.canvas.create_image(canvas_size[0]/2, canvas_size[1]/2, image=self._cached_images)
        print('Finished initial image caching')
        self.update_canvas()
        print(self._cached_images)


    def update_canvas(self):

        if not isinstance(self._cached_images[len(self._cached_images)//2], ImageTk.PhotoImage):
            # todo show error message
            pass
        else:
            if self._current_instance != None:
                self.canvas.delete(self._current_instance)

            canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
            self._current_instance = self.canvas.create_image(canvas_size[0]/2, canvas_size[1]/2, 
                                                              image=self._cached_images[len(self._cached_images)//2])
            # self._cached_images[len(self._cached_images)//2].
        
        # try: # try to open file as image
        #     img = Image.open(self.current_photos[self.current_index].path)
        # except UnidentifiedImageError: # display error message
        #     print('App could not open the image.')
        #     return

        # # todo display a message while image is loading, check if an image is currently loading

        # w2h = float(img.width)/img.height # width to height ratio
        # canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
        # if canvas_size[0]/canvas_size[1] > w2h:
        #     img = img.resize((int(canvas_size[1]*w2h), canvas_size[1]), Image.ANTIALIAS)
        # else:
        #     img = img.resize((canvas_size[0], int(canvas_size[0]/w2h)), Image.ANTIALIAS)
        # self._cached_images[CACHE_SIZE//2] = ImageTk.PhotoImage(img)
        # img_inst = self.canvas.create_image(canvas_size[0]/2, canvas_size[1]/2, image=self._cached_images)


    # todo have to use multithreading to load images in cache
