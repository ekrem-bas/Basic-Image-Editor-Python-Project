import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFilter, ImageDraw2

# Ekran
root = tk.Tk()
root.geometry("1000x600")
root.title("Image Editor")

# Varsayılan kalem rengi ve boyutu
pen_color = "Black"
pen_size = 5

# Global değişkenler
file_path = None
original_image = None
# processing image
processing_image = None
image_tk = None
draw = None
# ratio
ratio = 1
offset_x = 0
offset_y = 0

# crop
crop_rect = None
start_x = None
start_y = None

def resize_image(image, target_width, target_height):
    original_width, original_height = image.size
    global ratio, offset_x, offset_y
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image

def open_image():
    global original_image, image_tk, processing_image

    file_path = filedialog.askopenfilename(filetypes=[("JPEG Files", "*.jpeg"), ("PNG Files", "*.png")])
    if not file_path:
        return

    original_image = Image.open(file_path)
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    resized_image = resize_image(original_image, canvas_width, canvas_height)
    image_tk = ImageTk.PhotoImage(resized_image)
    processing_image = original_image.copy()

    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=image_tk)
    canvas.image = image_tk  # Referans tutarak görüntünün kaybolmasını engelle

def save_file():
    global processing_image

    save_file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpeg")])
    if not save_file_path:
        return
    
    # Resmin son halini kaydet
    # if filtering_image != original_image:
    #     save_image = filtering_image
    # else:
    #     save_image = drawing_image
    save_image = processing_image

    save_image.save(save_file_path)

def toggle_draw():
    if canvas.bind("<B1-Motion>"):
        canvas.unbind("<B1-Motion>")
    else:
        canvas.bind("<B1-Motion>", draw_on_image)
        
def draw_on_image(event):
    global processing_image, ratio, offset_x, offset_y, draw
    x, y = event.x - offset_x, event.y - offset_y
    x1, y1 = (x - pen_size), (y - pen_size)
    x2, y2 = (x + pen_size), (y + pen_size)
    canvas.create_oval(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, fill=pen_color, outline=pen_color)

    # Orijinal resimdeki koordinatları doğru şekilde ölçeklendirin
    draw = ImageDraw.Draw(processing_image)
    original_x1 = int(x1 / ratio)
    original_y1 = int(y1 / ratio)
    original_x2 = int(x2 / ratio)
    original_y2 = int(y2 / ratio)
    
    # Çizim boyutlarını orijinal boyutlara göre ayarlayın
    draw.ellipse([original_x1, original_y1, original_x2, original_y2], fill=pen_color, outline=pen_color)

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def change_pen_size(event=None):
    global pen_size
    pen_size = int(ps_spin_box.get())

def clear_canvas():
    global image_tk, original_image, processing_image, temp_image, image
    resized_image = resize_image(original_image, canvas.winfo_width(), canvas.winfo_height())
    image_tk = ImageTk.PhotoImage(resized_image)
    canvas.delete("all")
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor="center", image=image_tk)
    # eğer resimde drawing işlemi yapıldıysa drawing image resmini orijinalle değiştir

    processing_image = original_image.copy()
    temp_image = original_image.copy()
    image = original_image.copy()
    
def open_filter_menu():
        global filter_menu
        filter_menu = tk.Toplevel(root)
        filter_menu.geometry("250x350")
        filter_menu.title("Select a filter")
        filter_menu.config(bg= "white")
        
        # black and white button
        black_and_white_button = tk.Button(master= filter_menu, text= "Black and White", command= lambda : display_filter("Black and White"), highlightbackground= "white", fg= "black")
        black_and_white_button.pack(pady= 15)
        # blur button
        blur_button = tk.Button(master= filter_menu, text= "Blur", command= lambda : display_filter("Blur"), highlightbackground= "white", fg= "black")
        blur_button.pack(after= black_and_white_button)
        # sharpen button
        sharpen_button = tk.Button(master= filter_menu, text= "Sharpen", command= lambda : display_filter("Sharpen"), highlightbackground= "white", fg= "black")
        sharpen_button.pack(pady= 15)
        # smooth button
        smooth_button = tk.Button(master= filter_menu, text= "Smooth", command= lambda : display_filter("Smooth"), highlightbackground= "white", fg= "black")
        smooth_button.pack()
        # emboss button
        emboss_button = tk.Button(master= filter_menu, text= "Emboss", command= lambda : display_filter("Emboss"), highlightbackground="white", fg= "black")
        emboss_button.pack(pady= 15)
        # TODO : bu iki butonu yan yana koymak için bir küçük frame oluştur
        # apply button
        apply_button = tk.Button(master= filter_menu, text= "Apply Filter", command= apply_filter, highlightbackground="white", fg="Black")
        apply_button.pack()
        
        # clear filter button
        clear_button = tk.Button(master= filter_menu, text= "Clear", command= lambda : display_filter("Clear"), highlightbackground= "white", fg= "black")
        clear_button.pack()
        

def display_filter(filter_):
    global processing_image, temp_image, image
    # temp_image = drawing_image.copy()
    temp_image = processing_image.copy()
    image = resize_image(temp_image, canvas.winfo_width(), canvas.winfo_height())
    if filter_ == "Black and White":
        image = ImageOps.grayscale(image)
        temp_image = ImageOps.grayscale(processing_image)
    elif filter_ == "Blur":
        image = image.filter(ImageFilter.BLUR)
        temp_image = temp_image.filter(ImageFilter.BLUR)
    elif filter_ == "Sharpen":
        image = image.filter(ImageFilter.SHARPEN)
        temp_image = temp_image.filter(ImageFilter.SHARPEN)
    elif filter_ == "Smooth":
        image = image.filter(ImageFilter.SMOOTH)
        temp_image = temp_image.filter(ImageFilter.SMOOTH)
    elif filter_ == "Emboss":
        image = image.filter(ImageFilter.EMBOSS)
        temp_image = temp_image.filter(ImageFilter.EMBOSS)
    else:
        image = resize_image(temp_image, canvas.winfo_width(), canvas.winfo_height())
        filter_menu.destroy()
    image_tk = ImageTk.PhotoImage(image)
    canvas.delete("all")
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor="center", image=image_tk)
    canvas.image = image_tk 

def apply_filter():
    global processing_image, temp_image
    processing_image = temp_image
    filter_menu.destroy()

def toggle_crop():
    if canvas.bind("<ButtonPress-1>"):
        canvas.unbind("<ButtonPress-1>")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")
    else:
        canvas.bind("<ButtonPress-1>", start_crop)
        canvas.bind("<B1-Motion>", draw_crop_rectangle)
        canvas.bind("<ButtonRelease-1>", crop_image)

def start_crop(event):
    global start_x, start_y, crop_rect
    start_x, start_y = event.x, event.y
    if crop_rect:
        canvas.delete(crop_rect)
        crop_rect = None

def draw_crop_rectangle(event):
    global crop_rect
    if crop_rect:
        canvas.delete(crop_rect)
    end_x, end_y = event.x, event.y
    crop_rect = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red")

def crop_image(event):
    global original_image, processing_image, image_tk, ratio, offset_x, offset_y, crop_rect

    if not crop_rect:
        return

    x1 = min(start_x, event.x)
    y1 = min(start_y, event.y)
    x2 = max(start_x, event.x)
    y2 = max(start_y, event.y)

    x1 = max(0, x1 - offset_x)
    y1 = max(0, y1 - offset_y)
    x2 = min(canvas.winfo_width(), x2 - offset_x)
    y2 = min(canvas.winfo_height(), y2 - offset_y)

    original_x1 = int(x1 / ratio)
    original_y1 = int(y1 / ratio)
    original_x2 = int(x2 / ratio)
    original_y2 = int(y2 / ratio)

    cropped_image = processing_image.crop((original_x1, original_y1, original_x2, original_y2))

    original_image = original_image.crop((original_x1, original_y1, original_x2, original_y2))
    processing_image = cropped_image


    resized_image = resize_image(cropped_image, canvas.winfo_width(), canvas.winfo_height())
    image_tk = ImageTk.PhotoImage(resized_image)

    canvas.delete("all")
    canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor="center", image=image_tk)
    canvas.image = image_tk

    crop_rect = None

# Sol çerçeve
left_frame = tk.Frame(root, width=200, height=800, bg="white")
left_frame.pack(side="left", fill="y")

# Sağ çerçeve
right_frame = tk.Frame(root, width=1000, height=800, bg="white")
right_frame.pack(fill="both", expand=True)

# Canvas
canvas = tk.Canvas(right_frame, width=200, height=800, bg="grey", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Menü
image_button = tk.Button(master=left_frame, text="Add Image", highlightbackground="white", command=open_image)
image_button.pack(pady=15, padx=15)

color_button = tk.Button(master=left_frame, text="Change Pen Color", highlightbackground="white", command=change_color)
color_button.pack(padx=15)

pen_size_frame = tk.Frame(master=left_frame, bg="white")
pen_size_frame.pack(pady=15)

spinbox_label = tk.Label(pen_size_frame, text="Change Pen Size", bg="white", fg="black")
spinbox_label.pack()

ps_spin_box = tk.Spinbox(pen_size_frame, from_=1, to=10, command=change_pen_size, textvariable=tk.StringVar(value="5"), highlightbackground="white", background="white", foreground="black")
ps_spin_box.pack(padx=15)
ps_spin_box.bind("<Return>", change_pen_size)

draw_button = tk.Button(master=pen_size_frame, text="Toggle Draw", highlightbackground="white", command=toggle_draw)
draw_button.pack()

clear_canvas_button = tk.Button(master=left_frame, text="Clear", highlightbackground="white", command=clear_canvas)
clear_canvas_button.pack()

save_button = tk.Button(master=left_frame, text="Save", highlightbackground="white", command=save_file)
save_button.pack()

# filter menu
filter_button = tk.Button(left_frame, text= "Select a filter", highlightbackground= "white", command= open_filter_menu)
filter_button.pack()

# crop button
crop_button = tk.Button(left_frame, text="Toggle Crop", highlightbackground="white", command=toggle_crop)
crop_button.pack()

root.mainloop()