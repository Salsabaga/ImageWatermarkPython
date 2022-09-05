import tkinter as tk
from tkinter import ttk
import PIL.Image
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.image_preview = None
        self.file_text_placeholder = None
        self.title("Image Watermark")
        self.geometry("500x400")
        self.watermark_image = None
        self.upload_image = None
        self.create_widgets()

        self.filename = ""

    def create_widgets(self):
        app_title = ttk.Label(self, text="Imaging Watermark Application")
        app_title.grid(column=0, row=0, rowspan=2)
        self.upload_image = ttk.Button(self, text="Open", command=self.upload_action)
        self.upload_image.grid(column=1, row=0)
        self.watermark_image = ttk.Button(self, text="Add Watermark", command=self.text_to_image, state="disabled")
        self.watermark_image.grid(column=1, row=1)
        self.file_text_placeholder = ttk.Label(self, text="Selected File name is found here")
        self.file_text_placeholder.grid(column=0, row=2, columnspan=2)
        self.image_preview = tk.Canvas(width=300, height=300)
        self.image_preview.grid(column=0, row=3)
        print(self.file_text_placeholder.winfo_class())

    def upload_action(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
        style = ttk.Style()
        if self.filename == '':
            style.configure("Emergency.TButton", foreground="red")
            self.file_text_placeholder.config(text="No file selected", style="Emergency.TButton")
            raise Exception("Testing exception")
        else:
            img = self.filename
            style.configure("Emergency.TButton", foreground="Green")
            self.watermark_image['state'] = "normal"
            self.file_text_placeholder.config(text=img)
            im = Image.open(img)
            self.image_preview.image = ImageTk.PhotoImage(im.resize((300, 300)), PIL.Image.Resampling.LANCZOS)
            self.image_preview.create_image(0, 0, image=self.image_preview.image, anchor='nw')
            print(self.filename)

    def text_to_image(self):
        # with Image.open(current_image[len(current_image) - 1]).convert("RGBA") as base:
        img_fraction = 0.5
        with Image.open(self.filename).convert("RGBA") as base:
            print(base.size)
            bg = Image.new("RGBA", base.size, (255, 255, 255, 68))
            d = ImageDraw.Draw(bg)
            txt = "Danny Watermark"
            fontsize = 1
            font = ImageFont.truetype("arial.ttf", 100)
            while font.getsize(txt)[0] < img_fraction * base.size[0]:
                # iterate until the text size is just larger than the criteria
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)

            # optionally de-increment to be sure it is less than criteria
            fontsize -= 1
            font = ImageFont.truetype("arial.ttf", fontsize)
            d.text((base.size[0]/2 - 200, base.size[1]/2 - 200), text=txt, font=font, fill=(255, 255, 255, 200))
            out = Image.alpha_composite(base, bg)
            out.show()
