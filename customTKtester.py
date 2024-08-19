import shutil
import os
import customtkinter
from customtkinter import filedialog
from CustomTkinterMessagebox import CTkMessagebox

def move(src_dir, dst_dir, file_extension):
    for file in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)

        if os.path.isfile(src_path) and file.lower().endswith(file_extension):
            shutil.move(src_path, dst_path)
            print(f"Moved: {src_path} to {dst_path}")
        else:
            print(f"Skipped: {src_path} (Not a file or doesn't match extension)")

def copy(src_dir, dst_dir, file_extension):
    for file in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)

        if os.path.isfile(src_path) and file.lower().endswith(file_extension):
            shutil.copy2(src_path, dst_path)
            print(f"Copied: {file} to {dst_path}")
        else:
            print(f"Skipped: {file}")

def browse_src():
    source_directory = filedialog.askdirectory(title="Select a source directory")
    if source_directory:
        src_dir.set(source_directory)

def browse_dst():
    destination_directory = filedialog.askdirectory(title="Select a destination directory")
    if destination_directory:
        dst_dir.set(destination_directory)

def choose_extension(options):
    global file_extension, root
    file_extension.set(options[0])  # setting default value
    extension_menu = customtkinter.CTkOptionMenu(root, variable=file_extension, values=options)
    extension_menu.grid(row=2, column=1, padx=10, pady=5)

def perform_action():
    src = src_dir.get()
    dst = dst_dir.get()
    file_ext = file_extension.get().strip().lower()
    action = action_var.get()

    if not src or not dst or not file_ext:
        CTkMessagebox.messagebox(title="Error", text="Please fill the fields and select directories")
        return

    if action == "move":
        move(src, dst, file_ext)
    elif action == "copy":
        copy(src, dst, file_ext)
    else:
        CTkMessagebox.messagebox(title="Error", text="Invalid action")

def move_to_respective_folders(src_dir, ext_to_dir_map):
    for file in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file)

        if os.path.isfile(src_path):
            file_ext = os.path.splitext(file)[1].lower()
            dst_dir = ext_to_dir_map.get(file_ext)

            if dst_dir:
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                dst_path = os.path.join(dst_dir, file)
                shutil.move(src_path, dst_path)
                print(f"Moved: {src_path} to {dst_path}")
            else:
                print(f"No destination mapped for extension: {file_ext}")
        else:
            print(f"Skipped: {src_path} (Not a file)")

def perform_move_all():
    src = src_dir.get()
    drive = drive_var.get()

    if not src:
        CTkMessagebox.messagebox(title="Error", text="Please select a source directory")
        return

    ext_to_dir_map = {
        'C:': {
            '.pdf': 'C:\\DocumentsC\\PDF',
            '.jpg': 'C:\\PicturesC\\JPG',
            '.mp3': 'C:\\SoundsC\\MP3',
            '.mp4': 'C:\\VideosC\\MP4'
        },
        'G:': {
            '.pdf': 'G:\\DocumentsG\\PDF',
            '.jpg': 'G:\\PicturesG\\JPG',
            '.mp3': 'G:\\SoundsG\\MP3',
            '.mp4': 'G:\\VideosG\\MP4'
        },
        'H:': {
            '.pdf': 'H:\\DocumentsH\\PDF',
            '.jpg': 'H:\\PicturesH\\JPG',
            '.mp3': 'H:\\SoundsH\\MP3',
            '.mp4': 'H:\\VideosH\\MP4'
        },
        'F:': {
            '.pdf': 'F:\\DocumentsF\\PDF',
            '.jpg': 'F:\\PicturesF\\JPG',
            '.mp3': 'F:\\SoundsF\\MP3',
            '.mp4': 'F:\\VideosF\\MP4'
        }
    }

    if drive not in ext_to_dir_map:
        CTkMessagebox.messagebox(title="Error", text="Invalid drive selection")
        return

    move_to_respective_folders(src, ext_to_dir_map[drive])
    CTkMessagebox.messagebox(title="Success", text="Files have been moved to their respective folders", sound="no")

def main():
    global src_dir, dst_dir, file_extension, action_var, root, drive_var

    root = customtkinter.CTk()
    root.title("Mover")

    customtkinter.set_appearance_mode("dark")

    window_height = 400
    window_width = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    src_dir = customtkinter.StringVar()
    dst_dir = customtkinter.StringVar()
    file_extension = customtkinter.StringVar()
    action_var = customtkinter.StringVar(value="move")
    drive_var = customtkinter.StringVar(value="C:")

    customtkinter.CTkLabel(root, text="Source directory: ").grid(row=0, column=0, padx=10, pady=5)
    customtkinter.CTkEntry(root, textvariable=src_dir, width=150).grid(row=0, column=1, padx=10, pady=5)
    customtkinter.CTkButton(root, text="Browse", command=browse_src).grid(row=0, column=2, padx=10, pady=5)

    customtkinter.CTkLabel(root, text="Destination directory: ").grid(row=1, column=0, padx=10, pady=5)
    customtkinter.CTkEntry(root, textvariable=dst_dir, width=150).grid(row=1, column=1, padx=10, pady=5)
    customtkinter.CTkButton(root, text="Browse", command=browse_dst).grid(row=1, column=2, padx=10, pady=5)

    customtkinter.CTkLabel(root, text="File extension: (e.g., mp3, jpg, png): ").grid(row=2, column=0, padx=10, pady=5)
    choose_extension([".jpg", ".png", ".txt", ".mp3", ".pdf"])

    customtkinter.CTkRadioButton(root, text="Move", variable=action_var, value="move").grid(row=3, column=0, padx=10, pady=5)
    customtkinter.CTkRadioButton(root, text="Copy", variable=action_var, value="copy").grid(row=3, column=1, padx=10, pady=5)

    customtkinter.CTkLabel(root, text="Select drive: ").grid(row=4, column=0, padx=20, pady=5)
    drive_menu = customtkinter.CTkOptionMenu(root, variable=drive_var, values=["C:", "G:", "F:", "H:"])
    drive_menu.grid(row=4, column=1, padx=20, pady=5)

    customtkinter.CTkButton(root, text="Execute", command=perform_action).grid(row=5, column=0, padx=10, pady=5)

    customtkinter.CTkButton(root, text="Move all", command=perform_move_all).grid(row=6, column=0, padx=10, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()
