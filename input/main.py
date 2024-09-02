import cv2
from cvzone.FaceDetectionModule import FaceDetector
import os
from tkinter import Label, Button, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pathlib import Path

# Initialize the FaceDetector
detector = FaceDetector()

def get_next_output_folder(base_output_dir):
    # Find the last folder index
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

    # Determine a new output folder with a unique index
    output_dir = get_next_output_folder(base_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for image_filename in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_filename)

        if not image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue  # Skip non-image files

        # Load the image
        image = cv2.imread(image_path)

        # Create a copy of the original image to display later
        original_image = image.copy()

        # Detect faces in the image without drawing the percentage (detect=False)
        image, faces = detector.findFaces(image, draw=False)

        # Loop over the detected faces
        if faces:
            for face in faces:
                x, y, w, h = face['bbox']

                # Expand the face region a bit to avoid hard edges
                padding = 10
                x1, y1 = max(0, x - padding), max(0, y - padding)
                x2, y2 = min(image.shape[1], x + w + padding), min(image.shape[0], y + h + padding)

                # Extract the region of the face
                face_region = image[y1:y2, x1:x2]

                # Blur the face
                blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)

                # Replace the original face with the blurred face
                image[y1:y2, x1:x2] = blurred_face

        # Save the blurred image in the output directory
        output_image_path = os.path.join(output_dir, f'blurred_{image_filename}')
        cv2.imwrite(output_image_path, image)

        print(f"Processed image saved as {output_image_path}")

    # Show a completion notification
    messagebox.showinfo("Proses Selesai", "Proses blur wajah selesai. Hasil telah disimpan di folder output.")


def process_single_image(image_path):
    base_output_dir = 'output'
    os.makedirs(base_output_dir, exist_ok=True)

    # Determine a new output folder with a unique index
    output_dir = get_next_output_folder(base_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Load the image
    image = cv2.imread(image_path)

    # Detect faces in the image without drawing the percentage (detect=False)
    image, faces = detector.findFaces(image, draw=False)

    # Loop over the detected faces
    if faces:
        for face in faces:
            x, y, w, h = face['bbox']

            # Expand the face region a bit to avoid hard edges
            padding = 10
            x1, y1 = max(0, x - padding), max(0, y - padding)
            x2, y2 = min(image.shape[1], x + w + padding), min(image.shape[0], y + h + padding)

            # Extract the region of the face
            face_region = image[y1:y2, x1:x2]

            # Blur the face
            blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)

            # Replace the original face with the blurred face
            image[y1:y2, x1:x2] = blurred_face

    # Save the blurred image in the output directory
    output_image_path = os.path.join(output_dir, f'blurred_{Path(image_path).name}')
    cv2.imwrite(output_image_path, image)

    print(f"Processed image saved as {output_image_path}")

    # Show a completion notification
    messagebox.showinfo("Proses Selesai", "Proses blur wajah selesai. Hasil telah disimpan di folder output.")


def select_folder():
    input_dir = filedialog.askdirectory()
    if input_dir:
        process_images(input_dir)


def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if image_path:
        process_single_image(image_path)


def drag_and_drop(event):
    paths = root.tk.splitlist(event.data)
    for path in paths:
        if os.path.isdir(path):
            process_images(path)
        elif os.path.isfile(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            process_single_image(path)


# GUI
root = TkinterDnD.Tk()
root.title("Blur Faces in Images")
root.geometry("400x200")

label = Label(root, text="Pilih Folder atau Gambar untuk blur wajah")
label.pack(pady=20)

button_folder = Button(root, text="Select Folder", command=select_folder)
button_folder.pack(pady=10)

button_image = Button(root, text="Select Image", command=select_image)
button_image.pack(pady=10)

# fungsi drag-and-drop
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drag_and_drop)

root.mainloop()
