from tkinter import *
import tkinter.filedialog as fileDialog
from tkinter.messagebox import askyesno
from PIL import ImageTk, Image, UnidentifiedImageError
import os
from winsort import winsort

# count of images to store in cache
# has to be odd as the image currently loaded will 
# have equal number of next and previous images loaded in cache
CACHE_SIZE = 11

class PhotoManager:
    def __init__(self, window: Tk, canvas: Canvas):
        self.current_photos = list() # photos in current directory
        self.current_index = 0 # index of current photo in current_photos
        self.current_dir = None # current directory path
        self.window = window # tkinter window
        self.canvas = canvas # tkinter canvas
        self._cached_images = None # currently cached images
        self._current_instance = None # instance of currently shown image
        self.loading_text_instance = None # instance of a text shown while inspector is loading photo
        """  

        States:

        Idle - initial state, used when no photos were chosen yet or all photos in inspected directory were deleted
        Loading - used when requested images are being cached and can't be shown yet
        Viewing - used when requested image is loaded and is being shown to a viewer

        """
        self.state = 'Idle'

        self.window.update()

    # returns ImageTk.PhotoImage of current_photos[index], or str if error occured
    def _get_image(self, index):
        try: # try to open file as image
            img = Image.open(self.current_photos[index].path)
        except UnidentifiedImageError:
            return 'App could not open the image.'
        except PermissionError:
            return 'Permission to open that file denied.'
        
        # scaling to screen
        w2h = float(img.width)/img.height # width to height ratio
        canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
        if canvas_size[0]/canvas_size[1] > w2h:
            img = img.resize((int(canvas_size[1]*w2h), canvas_size[1]), Image.BICUBIC)
        else:
            img = img.resize((canvas_size[0], int(canvas_size[0]/w2h)), Image.BICUBIC)
        
        return ImageTk.PhotoImage(img)


    # changes state, does corresponding actions
    def change_state(self, state: str):
        if state == 'Loading' and self.state != 'Loading':
            canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
            self.loading_text_instance = self.canvas.create_text(canvas_size[0]/2, canvas_size[1]/2, 
                                                   text="Please wait...", font=('Lato', 18))
            self.canvas.update()
            self.state = 'Loading'
        elif state == 'Viewing' and self.state != 'Viewing':
            if self.loading_text_instance != None:
                self.canvas.delete(self.loading_text_instance)
                self.loading_text_instance == None
            self.state = 'Viewing'
        elif state == 'Idle' and self.state != 'Idle':
            self.change_state('Viewing')
            self.state == 'Idle'


    # initializes all containers via file/directory opening dialog
    def choose_photos(self, mode: str):
        if mode == 'dir': # choose directory
            self.current_dir = fileDialog.askdirectory(initialdir='/', title='Select directory...')
            if(self.current_dir == ''): # Cancelled choosing directory
                return
            
            self.change_state('Loading')
            self.current_photos = winsort([file for file in os.scandir(self.current_dir) if file.is_file()], 'name')
            for file in self.current_photos:
                print(file)
        else: # choose a photo
            temp = fileDialog.askopenfile(mode='r', initialdir='/', title='Select photo...')
            if(temp == None): # Cancelled choosing file
                return

            self.change_state('Loading')
            file_name = temp.name.split('/')[-1]
            self.current_dir = os.path.dirname(temp.name)
            self.current_photos = winsort([file for file in os.scandir(self.current_dir) if file.is_file()], 'name')
            for i in range(len(self.current_photos)):
                if(self.current_photos[i].name == file_name):
                    self.current_index = i
                    break
        
        # print(self.current_photos[self.current_index].path)
        self.cache_images()
    

    # moves currently selected photo to recycle bin
    def delete_current_photo(self):
        # pop everything, if left len < cache then rotate cache, else refill cache, change index, update canvas
        if len(self.current_photos) == 0:
            return
        if not askyesno('Delete', 'Are you sure you want to delete that photo?'):
            return
        # todo implement send2trash usage after all other features
        self.current_photos.pop(self.current_index)
        if CACHE_SIZE > len(self.current_photos): # less files than cache length
            self._cached_images.pop(len(self._cached_images)//2)
            if(len(self.current_photos) % 2 == 1): # rotating cache if needed
                self._cached_images.append(self._cached_images.pop(0))
            if len(self.current_photos) == self.current_index:
                self.current_index -= 1
        else:
            if len(self.current_photos) == self.current_index:
                self.current_index = (self.current_index - 1) % len(self.current_photos)
            index = (self.current_index+len(self._cached_images)//2) % len(self.current_photos)
            self._cached_images.pop(len(self._cached_images)//2)
            self._cached_images.append(self._get_image(index))
        
        self.update_canvas()


    # switches current photo to next/previous photo
    def switch_photo(self, direction: str):
        if len(self.current_photos) < 2 or self.state == 'Loading':
            return
        print(f'Initial switch information: \n index = {self.current_index} \n cache = \
                {self._cached_images} \n cache_size = {len(self._cached_images)}')
        if direction == 'Previous':
            if len(self.current_photos) < CACHE_SIZE: # no caching required, everything already is cached
                self._cached_images.insert(0, self._cached_images.pop())
                self.current_index = (self.current_index - 1) % len(self.current_photos)
                self.update_canvas()
            else:
                self._cached_images.pop()
                self.current_index = (self.current_index - 1) % len(self.current_photos)
                self._cached_images.insert(0, None)
                self.update_canvas()
                index = (self.current_index - CACHE_SIZE//2) % len(self.current_photos)
                self._cached_images[0] = self._get_image(index)
                print("finished caching image")
        else:
            if len(self.current_photos) < CACHE_SIZE: # no caching required, everything already is cached
                self._cached_images.append(self._cached_images.pop(0))
                self.current_index = (self.current_index + 1) % len(self.current_photos)
                self.update_canvas()
            else:
                self._cached_images.pop(0)
                self.current_index = (self.current_index + 1) % len(self.current_photos)
                self._cached_images.append(None)
                self.update_canvas()
                index = (self.current_index + CACHE_SIZE//2) % len(self.current_photos)
                self._cached_images[-1] = self._get_image(index)
                print("finished caching image")
        print(f'Afterwards switch information: \n index = {self.current_index} \n cache = \
                {self._cached_images} \n cache_size = {len(self._cached_images)}')

    
    # caches images for loading optimization, views initial photo
    def cache_images(self):
        if len(self.current_photos) == 0:
            self.change_state('Idle')
            self.update_canvas()
            return
        # initializing cache
        cache_size = CACHE_SIZE
        if len(self.current_photos) < CACHE_SIZE:
            cache_size = len(self.current_photos)
        self._cached_images = [None] * cache_size

        for i in range(cache_size):
            index = (self.current_index+i-(cache_size//2)) % len(self.current_photos)
            self._cached_images[i] = self._get_image(index)

            if i == cache_size // 2: # already cached requested image, can be shown
                self.update_canvas()
        print('Finished initial image caching')
        print(self._cached_images)


    # loads and views current photo
    def update_canvas(self):
        if self._current_instance != None:
            self.canvas.delete(self._current_instance)
            self._current_instance = None
        if len(self.current_photos) == 0: # no photos to show
            return
        canvas_size = (int(self.canvas['width']), int(self.canvas['height']))
        if not isinstance(self._cached_images[len(self._cached_images)//2], ImageTk.PhotoImage):
            error_text = 'Error'
            if isinstance(self._cached_images[len(self._cached_images)//2], str):
                error_text = self._cached_images[len(self._cached_images)//2]
            self._current_instance = self.canvas.create_text(canvas_size[0]/2, canvas_size[1]/2, 
                                                             text=error_text, font=('Lato', 18))
        else:
            self.change_state('Loading')
            self._current_instance = self.canvas.create_image(canvas_size[0]/2, canvas_size[1]/2, 
                                                              image=self._cached_images[len(self._cached_images)//2])
            self.change_state('Viewing')

        self.canvas.update()

    # todo have to use multithreading to load images in cache
