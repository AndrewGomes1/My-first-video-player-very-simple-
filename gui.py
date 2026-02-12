import os
import customtkinter

from ctypes import c_char_p
import ctypes
import threading

lib = ctypes.CDLL(r"C:\lib\cmake-build-debug\libvideo_player.dll")

lib.video_player.argtypes = [c_char_p]
lib.video_player.restype = int

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


    for i, video_path in enumerate(video_paths):

        v = video_path.split("\\")[-1]

        label = (customtkinter.CTkLabel(master=my_frame, text=v, font=("helvetica", 30), cursor="hand2"))
        label.grid(row=i, column=0, sticky="nsew")

        label.bind("<Enter>", lambda e, lbl=label: lbl.configure(fg_color="black"))
        label.bind("<Leave>", lambda e, lbl=label: lbl.configure(fg_color="#222222"))
        label.bind("<Button-1>", lambda e, path=video_path: on_click(path))

    app.mainloop()


if __name__ == "__main__":
    main()