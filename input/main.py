import cv2
from cvzone.FaceDetectionModule import FaceDetector
import os
from tkinter import Label, Button, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip

# Initialize the FaceDetector
detector = FaceDetector()


def get_next_output_folder(base_output_dir):
    existing_folders = [d for d in os.listdir(base_output_dir) if os.path.isdir(os.path.join(base_output_dir, d))]
    existing_folders.sort(reverse=True)

    if existing_folders:
        last_index = int(existing_folders[0].split('_')[-1])
        next_index = last_index + 1
    else:
        next_index = 1

    return os.path.join(base_output_dir, f'blurred_images_{next_index}')


def process_images(input_dir):
    base_output_dir = 'output'
    os.makedirs(base_output_dir, exist_ok=True)

    output_dir = get_next_output_folder(base_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for image_filename in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_filename)

        if not image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue  # Skip non-image files

        image = cv2.imread(image_path)
        original_image = image.copy()
        image, faces = detector.findFaces(image, draw=False)

        if faces:
            for face in faces:
                x, y, w, h = face['bbox']
                padding = 10
                x1, y1 = max(0, x - padding), max(0, y - padding)
                x2, y2 = min(image.shape[1], x + w + padding), min(image.shape[0], y + h + padding)
                face_region = image[y1:y2, x1:x2]
                blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
                image[y1:y2, x1:x2] = blurred_face

        output_image_path = os.path.join(output_dir, f'blurred_{image_filename}')
        cv2.imwrite(output_image_path, image)
        print(f"Processed image saved as {output_image_path}")

    messagebox.showinfo("Process Completed", "Face blurring completed. Results are saved in the output folder.")


def process_single_image(image_path):
    base_output_dir = 'output'
    os.makedirs(base_output_dir, exist_ok=True)

    output_dir = get_next_output_folder(base_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)
    image, faces = detector.findFaces(image, draw=False)

    if faces:
        for face in faces:
            x, y, w, h = face['bbox']
            padding = 10
            x1, y1 = max(0, x - padding), max(0, y - padding)
            x2, y2 = min(image.shape[1], x + w + padding), min(image.shape[0], y + h + padding)
            face_region = image[y1:y2, x1:x2]
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
            image[y1:y2, x1:x2] = blurred_face

    output_image_path = os.path.join(output_dir, f'blurred_{Path(image_path).name}')
    cv2.imwrite(output_image_path, image)
    print(f"Processed image saved as {output_image_path}")

    messagebox.showinfo("Process Completed", "Face blurring completed. Results are saved in the output folder.")


def blur_faces_in_frame(frame):
    # Copy the frame to make it writable
    modified_frame = frame.copy()

    image, faces = detector.findFaces(modified_frame, draw=False)
    if faces:
        for face in faces:
            x, y, w, h = face['bbox']
            padding = 10
            x1, y1 = max(0, x - padding), max(0, y - padding)
            x2, y2 = min(image.shape[1], x + w + padding), min(image.shape[0], y + h + padding)
            face_region = modified_frame[y1:y2, x1:x2]
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
            modified_frame[y1:y2, x1:x2] = blurred_face

    return modified_frame


def process_video(video_path):
    try:
        base_output_dir = 'output'
        os.makedirs(base_output_dir, exist_ok=True)

        output_dir = get_next_output_folder(base_output_dir)
        os.makedirs(output_dir, exist_ok=True)

        output_video_path = os.path.join(output_dir, f'blurred_{Path(video_path).name}')

        video_clip = VideoFileClip(video_path)

        # Apply blur effect on each frame
        blurred_clip = video_clip.fl_image(blur_faces_in_frame)

        # Write the processed video with audio
        blurred_clip.write_videofile(output_video_path, codec="libx264", audio=True)

        print(f"Processed video saved as {output_video_path}")

        messagebox.showinfo("Process Completed", "Face blurring completed. Results are saved in the output folder.")
    except Exception as e:
        print(f"Error processing video: {e}")
        messagebox.showerror("Error", f"Failed to process video: {e}")


def select_folder():
    input_dir = filedialog.askdirectory()
    if input_dir:
        process_images(input_dir)


def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if image_path:
        process_single_image(image_path)


def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if video_path:
        process_video(video_path)


def drag_and_drop(event):
    try:
        paths = root.tk.splitlist(event.data)
        for path in paths:
            if os.path.isdir(path):
                process_images(path)
            elif os.path.isfile(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                process_single_image(path)
            elif os.path.isfile(path) and path.lower().endswith(('.mp4', '.avi', '.mov')):
                process_video(path)
    except Exception as e:
        print(f"Error during drag and drop: {e}")
        messagebox.showerror("Error", f"Failed to process file: {e}")


# GUI
root = TkinterDnD.Tk()
root.title("Blur Faces in Images and Videos")
root.geometry("400x250")

label = Label(root, text="Select a Folder, Image, or Video to Blur Faces")
label.pack(pady=20)

button_folder = Button(root, text="Select Folder", command=select_folder)
button_folder.pack(pady=10)

button_image = Button(root, text="Select Image", command=select_image)
button_image.pack(pady=10)

button_video = Button(root, text="Select Video", command=select_video)
button_video.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drag_and_drop)

root.mainloop()
