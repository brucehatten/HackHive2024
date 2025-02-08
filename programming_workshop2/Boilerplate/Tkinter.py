import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import kaggle


# Download the dataset
kaggle.api.dataset_download_files("msambare/fer2013", path="fer2013", unzip=True)

print("Dataset downloaded successfully!")


# OpenCV Video Capture (initialize later)

cap = None  

def start_camera():
    global cap, lbl_video

    # Initialize OpenCV camera only when the user agrees
    cap = cv2.VideoCapture(0)
    
    # Create new window for the camera feed
    cam_window = tk.Toplevel(root)
    cam_window.title("Live Camera Feed")
    cam_window.configure(bg='#2e2e2e')
    cam_window.geometry("640x480")

    # Label to display video
    lbl_video = tk.Label(cam_window, bg='#2e2e2e')
    lbl_video.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Button to close the camera window
    btn_close = tk.Button(cam_window, text="Close", command=lambda: close_camera(cam_window), 
                          bg='#ff4d4d', fg='white', font=('Helvetica', 12, 'bold'), relief=tk.FLAT)
    btn_close.pack(pady=10)

    update_frame()  # Start updating frames

def update_frame():
    global cap, lbl_video

    if cap is None:
        return

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frame = Image.fromarray(frame)  # Convert to PIL Image
        img_tk = ImageTk.PhotoImage(frame)  # Convert to Tkinter format

        lbl_video.img_tk = img_tk  # Keep reference
        lbl_video.config(image=img_tk)

    lbl_video.after(10, update_frame)  # Schedule next frame update

def close_camera(window):
    global cap
    if cap:
        cap.release()
        cap = None
    window.destroy()

# Main Tkinter window
root = tk.Tk()
root.title("Boot Screen")
root.configure(bg='#1c1c1c')
root.geometry("400x300")

# Header Label
header = tk.Label(root, text="Welcome", bg='#1c1c1c', fg='white', 
                  font=('Helvetica', 20, 'bold'))
header.pack(pady=20)

# Button to ask user if they want to turn on the camera
btn = tk.Button(root, text="Start Camera", command=start_camera, 
                bg='#4caf50', fg='white', font=('Helvetica', 14, 'bold'), relief=tk.FLAT)
btn.pack(pady=20)

# Exit Button
exit_btn = tk.Button(root, text="Exit :)", command=root.quit, 
                     bg='#d9534f', fg='white', font=('Helvetica', 12, 'bold'), relief=tk.FLAT)
exit_btn.pack(pady=10)

root.mainloop()

# Release camera when closing
if cap:
    cap.release()
cv2.destroyAllWindows()





