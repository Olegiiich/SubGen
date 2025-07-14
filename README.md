# SubGen: Whisper-Powered Subtitle Generator (Offline)

---

## About the Project

**SubGen** is a powerful and intuitive desktop application for Windows, designed for fast and accurate generation of high-quality subtitles from any audio and video files. By integrating with the advanced Whisper AI model from OpenAI, SubGen provides exceptional speech recognition accuracy, regardless of the language type or accent.

A key advantage of SubGen is its ability to operate completely offline. Once downloaded and installed, the program doesn't require an internet connection to generate subtitles, ensuring full data privacy and independence from network stability.

---

## Key Features

* **High-Quality Subtitles:** Uses the powerful Whisper model to create accurate subtitles.
* **Multilingual Support:** Supports speech recognition and subtitle generation for audio/video in any language worldwide.
* **Full Offline Operation:** The program functions without an internet connection after the initial download.
* **User-Friendly Interface:** An intuitive graphical user interface (GUI) for easy navigation and use.
* **Diverse Format Support:** Processes popular audio and video formats.

---

## Download and Installation

Since the program includes a large AI model, its size exceeds GitHub's file upload limit (2 GB). Therefore, the executable file is available for download via external cloud storage.

1.  **Download the Executable:**
    Click the link below to download the program's ZIP archive:
    **[Download SubGen v1.0.zip (2.7 GB)](https://drive.google.com/file/d/1npooDmZgUxABuJ5RGkabPDKI3q_-AJox/view?usp=drive_link)**
    *(Please allow the file to download completely, given its size.)*

2.  **Extract the Archive:**
    After downloading, extract `sub_gen.zip` to a convenient location on your computer (e.g., your Desktop or "Programs" folder).

3.  **Launch the Application:**
    Open the extracted `sub_gen` folder and double-click the `sub_gen.exe` file to start the program.

---

## System Requirements

For stable operation of the SubGen application, the following system requirements are recommended:

* **Operating System:** Windows 10 (64-bit) or newer.
* **Processor:** Preferably Intel Core i5 / AMD Ryzen 5 or newer.
* **Random Access Memory (RAM):** Minimum 8 GB, 16 GB or more recommended for processing large files.
* **Free Disk Space:** Minimum 5 GB of free space (for installation and temporary files).
* **Graphics Card (GPU):** An NVIDIA discrete graphics card with CUDA support (recommended) will significantly speed up the subtitle generation process. The program will also run on a CPU, but slower.

---

## How to Use

1.  Launch `sub_gen.exe`.
2.  In the graphical interface, select the audio or video file for which you want to generate subtitles.
3.  Choose your desired settings (e.g., recognition language, if necessary).
4.  Click the "Generate Subtitles" (or similar) button.
5.  Wait for the process to complete. The generated subtitles will be saved in the specified location.

## For Developers (Running from Source)

If you wish to contribute to the project or run the application directly from its source code, follow these steps:

1.  **Clone the Repository:**
    Open your terminal (Command Prompt or PowerShell) and clone the project:
    ```bash
    git clone [https://github.com/Olegiiich/SubGen.git](https://github.com/Olegiiich/SubGen.git)
    cd SubGen
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv .venv
    ```
    * **On Command Prompt (cmd.exe):**
        ```bash
        .venv\Scripts\activate
        ```
    * **On PowerShell:**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```

3.  **Install Dependencies:**
    With the virtual environment active, install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    Once all dependencies are installed, you can run the application by executing your main script:
    ```bash
    python sub_gen.py
    ```
    *(**Note for Developers:** If your main script file is named something other than `sub_gen.py` (e.g., `main.py` or `app.py`), please adjust the command accordingly.)*

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
