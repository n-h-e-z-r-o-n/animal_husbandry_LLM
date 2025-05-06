# pip install pyspellchecker
# pip install pillow

# ========================================================= Required Imports  =============================================================

import tkinter as tk
import ctypes as ct # used for dark mode
import threading
from PIL import Image, ImageTk
import io
import base64
import re
import Retrieval_Augmented_Generation
import llm_inference


# ========================================================= Functions =====================================================================
# ========================================================= Global Variables  =============================================================


VIEW_BOX = QUERY_BT = INDICATOR = CHANGE_LLM = QUERY_ENTRY = D_HIDE = None
root = None
status = 0
shift_scroll = 0
grid_widgets = []
model_no = 1
display = 0


# ========================================================= Functions =====================================================================

def dark_title_bar(window):  # dark mode navegation bar
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


def imagen(image_path, screen_width, screen_height, widget): # image processing
    def load_image():
        try:
            image = Image.open(image_path)
        except Exception as e:
            try:
                image = Image.open(io.BytesIO(image_path))
            except Exception as e:
                print(e)
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()


def ask_binary_choice():
    global CHANGE_LLM, model_no, status
    if status == 1:
        return
    if model_no == 2:
        CHANGE_LLM.config(text="Fine_tuned only")
        model_no = 1
    elif model_no == 1:
        CHANGE_LLM.config(text="Fine tuned + RAG")
        model_no = 2
    else:
        pass


def Request_Info(user_query): #
    print("seraching")

    global display
    if display == 0:
        display_hide_chats()

    def start(user_query=user_query):
        global VIEW_BOX, QUERY_BT, model_no, status, INDICATOR
        if status == 1:
            return
        else:
            if str(user_query) == "":
                INDICATOR.config(bg="red")
                return
            else:
                 status = 1
                 INDICATOR.config(bg="green")

        print(user_query)

        VIEW_BOX.config(state=tk.NORMAL)
        VIEW_BOX.insert(tk.END, f"\n{user_query}\n", 'user_config')
        VIEW_BOX.see(tk.END)  # Scroll to the end of the text widget
        VIEW_BOX.config(state=tk.DISABLED)

        QUERY_BT.config(text="▫▫▫▫", fg="white")

        if model_no == 1:
            answer = llm_inference.llm_chain.run(Instruction=str(f"respond to this: {user_query}"))
        else:
            answer = Retrieval_Augmented_Generation.LLM_Run(str(user_query))

        VIEW_BOX.config(state=tk.NORMAL)
        VIEW_BOX.insert(tk.END, f"\n{answer}\n", 'llm_config')
        VIEW_BOX.see(tk.END)  # Scroll to the end of the text widget
        VIEW_BOX.config(state=tk.DISABLED)

        QUERY_BT.config(text="►", fg="white")
        status = 0
    threading.Thread(target=start).start()


def display_hide_chats():
    global VIEW_BOX, D_HIDE, display
    print("change", display)
    if display == 0:
        D_HIDE.config(text="<")
        VIEW_BOX.place(relx=0, rely=0, relheight=1, relwidth=1)
        display = 1
    elif  display == 1:
        D_HIDE.config(text=">")
        VIEW_BOX.place_forget()
        display = 0



# ========================================================= Main Function =================================================================

def main():
    global VIEW_BOX, QUERY_BT, CHANGE_LLM, INDICATOR, D_HIDE , QUERY_ENTRY
    # bg_color = "#1B1B1B"
    # bg_color = "#212122"
    bg_color = "#1F201F"

    app = tk.Tk()
    app.wm_attributes("-transparentcolor", "blue")
    app.config(bg=bg_color)
    app.iconbitmap("./assets/ICON.ico")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    app_width = 950
    app_height = 700
    #app.maxsize(app_width, app_height)
    app.minsize(app_width, app_height)
    app.title('LLM')
    # app.attributes("-toolwindow", 1)
    # app.attributes("-topmost", 1)
    # app.overrideredirect(True)
    dark_title_bar(app)



    on_c = '#2B3230'
    of_c = '#2B2B2C'
    fg_color = 'gray'

    BACKGROUND = tk.Label(app)
    BACKGROUND.place(relheight=1, relwidth=1, relx=0, rely=0)
    imagen("./assets/bg_image.jpg", app_width, app_height, BACKGROUND)

    TITAL = tk.Label(app, text='ANIMAL HUSBANDRY', fg="gray", compound = tk.CENTER,   font=("Georgia", 23, "bold"), bg=bg_color, borderwidth=0, border=0)
    TITAL.place(relx=0.15, rely=0, relheight=0.15, relwidth=0.7)
    imagen("./assets/title.png", int(app_width * 0.7), int(app_height * 0.15), TITAL)

    VIEW_BOX_canvas = tk.Label(app, bg=bg_color, borderwidth=0, border=0)
    VIEW_BOX_canvas.place(relx=0.05, rely=0.1, relheight=0.7, relwidth=0.9)
    imagen("./assets/bg_image2.png", int(app_width*0.9), int(app_height*0.7), VIEW_BOX_canvas)

    VIEW_BOX = tk.Text(VIEW_BOX_canvas, bg=bg_color, borderwidth=0, border=0, font=(13), wrap="word")
    VIEW_BOX.tag_configure("user_config", foreground="#B2BEB5", justify=tk.LEFT)  # user queries  config's
    VIEW_BOX.tag_configure("llm_config", foreground="#54626F", justify=tk.LEFT)  # llm responses config's
    VIEW_BOX.config(state=tk.DISABLED)

    D_HIDE = tk.Button(app, bg=bg_color, text=">", fg="white", compound=tk.CENTER, activebackground=bg_color, anchor="w", font=("Georgia", 12, "bold"), borderwidth=0, border=0, command=lambda : display_hide_chats())
    D_HIDE.place(relx=0.001, rely=0.45, relwidth=0.02, relheight=0.05)
    imagen("./assets/bt1.png", int(app_width * 0.02), int(app_height * 0.5), D_HIDE)

    CHANGE_LLM = tk.Button(app, bg='white', fg="white", text="Fine_tuned only", compound = tk.CENTER, activebackground=bg_color, anchor="w", font=("Courier New", 12, "bold"), borderwidth=0, border=0, command = lambda: ask_binary_choice())
    CHANGE_LLM.place(relx=0.05, rely=0.865, relwidth=0.25, relheight=0.04)
    imagen("./assets/button_bg.png", int(app_width*0.25), int(app_height*0.04), CHANGE_LLM)

    QUERY_ENTRY = tk.Entry(app, bg=of_c, fg="gray", insertbackground='white', justify=tk.CENTER, font=("Courier New", 12, "italic"), borderwidth=0, border=0)
    QUERY_ENTRY.place(relx=0.05, rely=0.92, relwidth=0.9, relheight=0.07)
    QUERY_ENTRY.bind("<Return>", lambda e: Request_Info(QUERY_ENTRY.get()))

    QUERY_BT = tk.Button(app, bg=bg_color,   activebackground=bg_color, compound = tk.CENTER, fg="white", text="►", font=("BOLD", 13), borderwidth=0, border=0, command=lambda: Request_Info(QUERY_ENTRY.get()))
    QUERY_BT.place(relx=0.965, rely=0.92, relheight=0.07, relwidth=0.03)
    imagen("./assets/button_bg2.png", int(app_width * 0.03), int(app_height * 0.07), QUERY_BT)

    INDICATOR = tk.Label(app, bg="green", borderwidth=0, border=0)
    INDICATOR.place(relx=0.3, rely=0.994, relwidth=0.4, relheight=0.002)

    def print_window_size(event=None):
        dynamic_width = app.winfo_width()
        dynamic_height = app.winfo_height()

        imagen("./assets/bg_image.jpg", dynamic_width, dynamic_height, BACKGROUND)
        imagen("./assets/title.png", int(dynamic_width * 0.7), int(dynamic_height * 0.15), TITAL)
        imagen("./assets/button_bg2.png", int(dynamic_width * 0.03), int(dynamic_height * 0.07), QUERY_BT)
        imagen("./assets/bg_image2.png", int(dynamic_width * 0.9), int(dynamic_height * 0.7), VIEW_BOX_canvas)
        imagen("./assets/bt1.png", int(dynamic_width * 0.02), int(dynamic_height * 0.5), D_HIDE)
        imagen("./assets/button_bg.png", int(dynamic_width * 0.25), int(dynamic_height * 0.04), CHANGE_LLM)

    BACKGROUND.bind("<Configure>", print_window_size)
    app.mainloop()


if __name__ == "__main__":
    main()
