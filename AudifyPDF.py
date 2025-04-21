import os
import threading
from tkinter import filedialog
import customtkinter as ctk
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import pyttsx3

""""
Python code to extract the content of pdf files as text and then converting that text 
to an .mp3 audio file the gets diposited in the audio_files directory
"""

# PDF settings
filepath = ""
MAX_PAGES = 20

# Setup customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create main window
root = ctk.CTk()
root.geometry("500x350")
root.resizable(False, False)
root.title("AudifyPDF - Text to Audio")

frame = ctk.CTkFrame(master=root, corner_radius=15, fg_color="#1e1e1e")
frame.pack(fill="both", expand=True, padx=0, pady=0)

# Title
titleLabel = ctk.CTkLabel(
    master=frame,
    text=" AudifyPDF \n 📄 PDF to 🎧 Audio Converter",
    font=("Arial", 20, "bold"),
    text_color="#FFFFFF",
)
titleLabel.pack(padx=10, pady=(20, 5))

subtitleLabel = ctk.CTkLabel(
    master=frame,
    text="Convert text from a PDF into an MP3 file.",
    font=("Arial", 13),
    text_color="#AFAFAF",
)
subtitleLabel.pack(pady=(0, 10))


# Thread runner
def run_in_thread(func):
    threading.Thread(target=func, daemon=True).start()


# Import Button
importFileButton = ctk.CTkButton(
    master=frame,
    text="📂 Import PDF File",
    width=320,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=lambda: run_in_thread(import_pdf_file),
)
importFileButton.pack(pady=6)

# Filename Entry
inputwindowName = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter output filename (e.g. myaudio.mp3)",
    width=320,
    height=40,
    font=("Arial", 12),
    justify="center",
    corner_radius=10,
)
inputwindowName.pack(pady=6)

# Convert Button
convertButton = ctk.CTkButton(
    master=frame,
    text="🔁 Convert to Audio",
    width=320,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    command=lambda: run_in_thread(convert),
)
convertButton.pack(pady=6)

# Notification Label
notificationLabel = ctk.CTkLabel(
    master=frame,
    text="",
    width=320,
    height=60,
    font=("Arial", 12),
    text_color="white",
    wraplength=300,
    justify="center",
)
notificationLabel.pack(pady=(6, 15))


# File Import Logic
def import_pdf_file():
    global filepath

    selected_file = filedialog.askopenfilename()
    if not selected_file:
        return
    if not selected_file.lower().endswith(".pdf"):
        notificationLabel.configure(
            text="Invalid file format. Please select a PDF.", text_color="red"
        )
        return

    if sum(1 for _ in extract_pages(selected_file)) > MAX_PAGES:
        notificationLabel.configure(
            text="PDF too long. Max 20 pages allowed.", text_color="orange"
        )
        return

    filepath = selected_file
    filename = os.path.basename(filepath)
    notificationLabel.configure(text=f"Imported: {filename}", text_color="green")


# Convert Logic
def convert():
    global filepath

    if filepath == "":
        notificationLabel.configure(text="No file selected!", text_color="red")
        return

    filename = inputwindowName.get().strip()
    if filename == "":
        notificationLabel.configure(text="Please enter a filename.", text_color="red")
        return
    if not filename.lower().endswith(".mp3"):
        filename += ".mp3"

    text = extract_text_from_pdf(filepath)
    if not text.strip():
        notificationLabel.configure(
            text=" No readable text found in the PDF.", text_color="orange"
        )
        return

    output_path = os.path.join("audio_files", filename)
    convert_text_to_audio(text, output_path)


# Text Extraction
def extract_text_from_pdf(given_filepath) -> str:
    text_output = ""

    for page_layout in extract_pages(given_filepath):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_output += element.get_text()

    return text_output


# Audio Conversion
def convert_text_to_audio(pdf_text, output_path):
    notificationLabel.configure(text="Converting ...", text_color="blue")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        engine = pyttsx3.init()
        engine.save_to_file(pdf_text, output_path)
        engine.runAndWait()

        notificationLabel.configure(
            text=f"Audio saved to:\n{output_path}", text_color="green"
        )
        try:
            os.startfile(os.path.dirname(output_path))
        except:
            pass
    except Exception as e:
        notificationLabel.configure(text=f"Error: {str(e)}", text_color="red")


root.mainloop()
