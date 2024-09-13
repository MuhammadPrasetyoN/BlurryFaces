# BlurryFaces

BlurryFaces is a Python project designed to automatically detect faces in images and apply a blur effect to them. This project uses OpenCV and the `cvzone.FaceDetectionModule` for face detection.

## Features
- Automatically detect and blur faces in images.
- Process entire folders of images or individual images.
- Supports drag-and-drop functionality for easy processing.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/BlurWajah.git
   cd BlurWajah
    ```
2.  **Create and activate a virtual environment**
    
- #### For Terminal User:
    
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
- #### PyCharm Users: 

    1. Open your project in PyCharm.
    2. Go to File > Settings (or PyCharm > Preferences on macOS).
    3. Navigate to `Project: <Your Project Name>` > `Python Interpreter`.
    4. Click the gear icon and select `Add....`
    5. Choose `Virtualenv Environment` and select `New environment.`
    6. Click `OK` to create and activate the virtual environment. PyCharm will handle the activation automatically.

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
## USAGE
    
### Using Terminal

 1. Open the terminal and navigate to the project directory.
 2. Run the script:
 
    ```bash
    python input/main.py
    ```

### Using pycharm or vscode
1. Open the project in your preferred IDE (PyCharm or VSCode).

2. Locate the main.py file in the input folder.

3. Click the Run button to execute the script.

--------
### GUI Instructions
4. The GUI window will appear once the script is running.
5. You can select Folder or Image, You can either select an entire folder of images or a single image file.
6. The processed images will be saved in the output folder.


## EXAMPLE

### Input Image:
![Output Image](/asset/example_input.png)

### Output Image:
![Output Image](/asset/example_output.png)

### Output Video:
 
![Output Video](/asset/the_rock%20meme.gif)

![Output Video](/asset/anya_waku.gif)

The above example demonstrates how the script successfully detects and blurs faces in an image.

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.