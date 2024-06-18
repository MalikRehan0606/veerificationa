import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from PIL import Image, ImageTk,ImageChops,ImageStat

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("image files", "*.jpeg;*.png;*.jpg"),
        ("all files", "*.*")
    ])
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("Capture Image")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Capture Image", frame)
        
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # Space pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            if sign == 1:
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            break

    cam.release()
    cv2.destroyAllWindows()

def capture_image(ent, sign=1):
    ent.delete(0, tk.END)
    ent.insert(tk.END, "Capturing image... Please press Space to capture and ESC to exit.")
    capture_image_from_cam_into_temp(sign=sign)

def calculate_similarity(img1, img2):
    # Open and convert images to grayscale
    img1 = Image.open(img1).convert('L')
    img2 = Image.open(img2).convert('L')

    # Resize images if necessary (adjust as per your requirements)
    img1 = img1.resize((300, 300))
    img2 = img2.resize((300, 300))

    # Calculate pixel-wise absolute difference
    diff = ImageChops.difference(img1, img2)

    # Calculate RMS (Root Mean Square) of the pixel differences
    rms_diff = ImageStat.Stat(diff).rms[0]

    # Normalize RMS to a similarity percentage
    similarity = 100 - rms_diff * 100 / 255

    return similarity

def check_similarity(window, path1, path2):
    result = calculate_similarity(path1, path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match",
                             f"Signatures are {result:.2f}% similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match",
                            f"Signatures are {result:.2f}% similar!!")
    return True

def create_gui():
    root = tk.Tk()
    root.title("Signature Matching")
    root.geometry("600x400")

    # Label for file path entry
    lbl_path1 = tk.Label(root, text="Signature Image 1:")
    lbl_path1.pack(pady=10)

    # Entry for file path 1
    ent_path1 = tk.Entry(root, width=50)
    ent_path1.pack()

    # Browse button for file path 1
    btn_browse1 = tk.Button(root, text="Browse", command=lambda: browsefunc(ent_path1))
    btn_browse1.pack()

    # Label for file path entry
    lbl_path2 = tk.Label(root, text="Signature Image 2:")
    lbl_path2.pack(pady=10)

    # Entry for file path 2
    ent_path2 = tk.Entry(root, width=50)
    ent_path2.pack()

    # Browse button for file path 2
    btn_browse2 = tk.Button(root, text="Browse", command=lambda: browsefunc(ent_path2))
    btn_browse2.pack()

    # Capture image buttons
    btn_capture1 = tk.Button(root, text="Capture Image 1", command=lambda: capture_image(ent_path1, sign=1))
    btn_capture1.pack(pady=10)

    btn_capture2 = tk.Button(root, text="Capture Image 2", command=lambda: capture_image(ent_path2, sign=2))
    btn_capture2.pack(pady=10)

    # Check similarity button
    btn_check = tk.Button(root, text="Check Similarity", command=lambda: check_similarity(root, ent_path1.get(), ent_path2.get()))
    btn_check.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
