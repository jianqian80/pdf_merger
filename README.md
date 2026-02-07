# Smart PDF & Image Merger (CLI)

A powerful Python command-line tool designed to merge PDFs and images (PNG, JPG, JPEG) into a single, professional document. It respects folder hierarchies and automatically centers images on A4 pages at high resolution.

## 🚀 Key Features

* **Recursive Merging:** Automatically enters sub-folders, merges their contents, and places them in order within the main document.
* **Image Support:** Converts PNG, JPG, JPEG, and WebP into PDF pages on the fly.
* **High Quality:** Images are rendered at **300 DPI** for professional print quality.
* **A4 Auto-Centering:** Images are resized to half-A4 size and centered perfectly with white margins.
* **Sequential Sorting:** Respects numerical prefixes (e.g., 01_Intro, 02_Chapter) for both files and folders.

---

## 🛠 Installation

1. **Clone or move** this folder to your desired location.
2. **Activate** your Python virtual environment.
3. **Install** the package in editable mode:

```bash
pip install -e .
```
This will automatically install the necessary dependencies (`PyPDF2` and `Pillow`) and register the `pdfmerge` command to your environment.

## 📖 Usage

Once the package is installed in your environment, you can run the tool from any directory in your terminal using the following commands:

### 1. Basic Merge
Merge everything in the current folder into Master_Combined.pdf:
```bash
pdfmerge .
```


### 2. Custom Output
Specify the folder to process and the name of the final file:
```bash
pdfmerge /path/to/your/files -o Final_Report.pdf
```

### 3. Help Menu
```bash
pdfmerge --help
```

---

## 📂 Expected Folder Structure
The tool is designed to handle structures like this:

```plaintext
Project_Folder/
├── 01_Cover.pdf
├── 02_Receipts/          <-- Sub-folders are merged into a block
│   ├── invoice1.jpg
│   └── invoice2.png
├── 03_Appendix.pdf
└── 04_Screenshot.png     <-- Images are centered on A4 pages
```

**Result:** A single PDF containing the Cover, followed by all receipts from the sub-folder, followed by the Appendix, and finally the Screenshot.

---

## 🔧 Technical Details

* **Resolution:** 300 DPI (2479 x 3508 pixels for A4).
* **Resampling:** Uses LANCZOS (High-quality downscaling).
* **PDF Logic:** Uses io.BytesIO streams to handle nested folder merging without creating temporary files on your disk.