import tkinter as tk
import ctypes as ct
import threading
from PIL import Image, ImageTk
import io, socket
import base64
import RAG
import Test_LLM




VIEW_BOX = QUERY_BT= None
root = None
client_socket = None
shift_scroll = 0
grid_widgets = []


# ----------------------------------------------------------------------------------------------------------------------

def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


def imagen(image_path, screen_width, screen_height, widget):
    def load_image():
        try:
            image = Image.open(image_path)
        except:
            try:
                image = Image.open(io.BytesIO(image_path))
            except:
                binary_data = base64.b64decode(image_path)  # Decode the string
                image = Image.open(io.BytesIO(binary_data))

        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        widget.config(image=photo)
        widget.image = photo  # Keep a reference to the PhotoImage to prevent it from being garbage collected

    image_thread = threading.Thread(target=load_image)  # Create a thread to load the image asynchronously
    image_thread.start()


def Request_Info(user_query):
    def start(user_query=user_query):
        global VIEW_BOX, QUERY_BT
        global client_socket

        VIEW_BOX.config(state=tk.NORMAL)
        VIEW_BOX.insert(tk.END,  f"\n{user_query}\n", 'user_config')
        VIEW_BOX.see(tk.END)  # Scroll to the end of the text widget
        VIEW_BOX.config(state=tk.DISABLED)


        QUERY_BT.config(state=tk.DISABLED)

        answer = RAG.LLM_Run(str(user_query))

        VIEW_BOX.config(state=tk.NORMAL)
        VIEW_BOX.insert(tk.END, f"\n{answer}\n", 'llm_config')
        VIEW_BOX.see(tk.END)  # Scroll to the end of the text widget
        VIEW_BOX.config(state=tk.DISABLED)

        QUERY_BT.config(state=tk.NORMAL)

    threading.Thread(target=start).start()

def main():
    global VIEW_BOX, QUERY_BT
    # bg_color = "#1B1B1B"
    # bg_color = "#212122"
    bg_color = "#1F201F"
    app = tk.Tk()

    app.config(bg=bg_color)
    app.maxsize(950, 700)
    app.minsize(950, 700)
    app.title('')
    # app.attributes("-toolwindow", 1)
    # app.attributes("-topmost", 1)
    dark_title_bar(app)

    on_c = '#2B3230'
    of_c = '#2B2B2C'
    fg_color = 'gray'

    VIEW_BOX = tk.Frame(app, bg=bg_color, borderwidth=0, border=0)
    VIEW_BOX.place(relx=0.05, rely=0.1, relheight=0.7, relwidth=0.9)
    #VIEW_DISPLAY, welcome_page_root = attach_scroll(VIEW_BOX)

    VIEW_BOX = tk.Text(VIEW_BOX, bg=bg_color, borderwidth=0, border=0, font=( 13))
    VIEW_BOX.place(relx=0.05, rely=0.1, relheight=0.7, relwidth=0.9)
    VIEW_BOX.tag_configure("user_config", foreground="#B2BEB5", justify=tk.LEFT )  # user queries  config's
    VIEW_BOX.tag_configure("llm_config", foreground="#54626F", justify=tk.RIGHT)  # llm responses config's
    VIEW_BOX.config(state=tk.DISABLED)

    QUERY_ENTRY = tk.Entry(app, bg=of_c, fg="gray", insertbackground='white', justify=tk.CENTER, font=("Courier New", 12, "italic"), borderwidth=0, border=0)
    QUERY_ENTRY.place(relx=0.05, rely=0.92, relwidth=0.9, relheight=0.07)

    QUERY_BT = tk.Button(app, bg=bg_color, activebackground=bg_color, fg="gray", text="►", font=("BOLD", 13), borderwidth=0, border=0, command=lambda:  Request_Info(QUERY_ENTRY.get()))
    QUERY_BT.place(relx=0.965, rely=0.92, relheight=0.07, relwidth=0.03)

    def on_closing():
        global client_socket
        client_socket.close()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()