import os
import customtkinter
import cv2
from PIL import Image

from ctypes import c_char_p
import ctypes
import threading

lib = ctypes.CDLL(r"C:\lib\cmake-build-debug\libvideo_player.dll")

lib.video_player.argtypes = [c_char_p]
lib.video_player.restype = int

video_widgets = []

THUMB_DIR = "thumbnails"
os.makedirs(THUMB_DIR, exist_ok=True)

def main():

    # The GUI

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    app = customtkinter.CTk()
    app.geometry("600x500")
    app.title("Video Streaming Application")

    video_paths = scann()

    my_frame = customtkinter.CTkScrollableFrame(app, label_text="Videos", label_font=("helvetica", 30))
    my_frame.pack(fill="both", expand=True)

    #for c in range(2):
    #    my_frame.grid_columnconfigure(c, weight=2)


    for i, video_path in enumerate(video_paths):

        thumb_path = get_thumb_path(video_path)

        if not os.path.exists(thumb_path):
            generate_thumbnail(video_path, thumb_path)

        img = Image.open(thumb_path)
        img = img.resize((300, 180))
        ctk_img = customtkinter.CTkImage(light_image=img, size=(300, 180))

        frame = customtkinter.CTkFrame(my_frame)

        #row = i // 2
        #col = i % 2

        label = customtkinter.CTkLabel(master=frame, text="", image=ctk_img, cursor="hand2")
        label.grid(row=0, column=0)

        label.bind("<Button-1>", lambda e, path=video_path: on_click(path))

        video_widgets.append(frame)

    # dynamic grid layout
    def update_grid(_event=None):

        for widget in video_widgets:
            widget.grid_forget()

        width = my_frame.winfo_width()

        thumb_width = 300  # thumbnail width + padding
        columns = max(1, width // thumb_width)

        for j, widget in enumerate(video_widgets):
            row = j // columns
            col = j % columns
            widget.grid(row=row, column=col, padx=15, pady=15)

        for c in range(columns):
            my_frame.grid_columnconfigure(c, weight=1)


    my_frame.bind("<Configure>", update_grid)
    app.after(100, lambda : update_grid())

    app.mainloop()



def get_thumb_path(video_path):
    base = os.path.splitext(os.path.basename(video_path))[0]
    return os.path.join(THUMB_DIR, base + ".jpg")

def generate_thumbnail(video_path, thumb_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = int(total_frames * 0.1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    success, frame = cap.read()

    if success:
        cv2.imwrite(thumb_path, frame)

    cap.release()
    return success

def video_start(path):
    lib.video_player(path.encode('utf-8'))

def on_click(path):
    threading.Thread(target=video_start, daemon=True, args=(path,)).start()

def scann():

    # scanning for video files

    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv')
    video_paths = []

    users_root = r"C:\Users"

    for user in os.listdir(users_root):
        user_path = os.path.join(users_root, user)

        if not os.path.isdir(user_path):
            continue

        folders_to_scan = [
            os.path.join(user_path, "Videos"),
            os.path.join(user_path, "Downloads"),
            os.path.join(user_path, "Desktop"),
        ]

        for folder in folders_to_scan:
            if not os.path.exists(folder):
                continue

            for root, dirs, files in os.walk(folder, onerror=lambda e: None):
                for file in files:
                    if file.lower().endswith(video_extensions):
                        video_paths.append(os.path.join(root, file))


    return video_paths

if __name__ == "__main__":
    main()
