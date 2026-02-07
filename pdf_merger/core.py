import PyPDF2
import os
import argparse
from PIL import Image
import io


def convert_image_to_pdf(image_path):
    # A4 dimensions in points
    A4_WIDTH_PTS = 595
    A4_HEIGHT_PTS = 842
    
    # Increase DPI for high-quality output (300 is standard for print/high-res)
    DPI = 300
    # Conversion factor from points to pixels: (DPI / 72)
    scale = DPI / 72.0
    
    # Calculate A4 dimensions in pixels for the canvas
    canvas_width_px = int(A4_WIDTH_PTS * scale)
    canvas_height_px = int(A4_HEIGHT_PTS * scale)
    
    # Target image size: Half of the A4 pixel dimensions
    target_width_px = canvas_width_px 
    target_height_px = canvas_height_px 

    img = Image.open(image_path)
    # Use LANCZOS for the highest quality downscaling
    img.thumbnail((target_width_px, target_height_px), Image.Resampling.LANCZOS)
    
    # Create high-res white canvas
    canvas = Image.new('RGB', (canvas_width_px, canvas_height_px), (255, 255, 255))
    
    # Center the high-res image
    x = (canvas_width_px - img.width) // 2
    y = (canvas_height_px - img.height) // 2
    canvas.paste(img, (x, y))
    
    # Save with the specified DPI so the PDF viewer knows the physical size
    pdf_buffer = io.BytesIO()
    canvas.save(pdf_buffer, format="PDF", resolution=float(DPI))
    pdf_buffer.seek(0)
    return pdf_buffer

# def convert_image_to_pdf(image_path):
#     # A4 Dimensions in points
#     A4_WIDTH = 595
#     A4_HEIGHT = 842
    
#     # Target size: Half of A4
#     TARGET_WIDTH = A4_WIDTH 
#     TARGET_HEIGHT = A4_HEIGHT

#     # Open image and convert to RGB
#     img = Image.open(image_path)
#     img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
    
#     # Create a white A4 canvas
#     canvas = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
    
#     # Calculate centering coordinates
#     # Formula: (Canvas_Size - Image_Size) / 2
#     x = (A4_WIDTH - img.width) // 2
#     y = (A4_HEIGHT - img.height) // 2
    
#     # Paste image onto white background
#     canvas.paste(img, (x, y))
    
#     # Save to memory buffer
#     pdf_buffer = io.BytesIO()
#     canvas.save(pdf_buffer, format="PDF", resolution=72.0)
#     pdf_buffer.seek(0)
#     return pdf_buffer

# def convert_image_to_pdf(image_path):
#     """Converts an image to a PDF file-like object in memory."""
#     img = Image.open(image_path)
#     img_converted = img.convert('RGB') # Ensures compatibility (especially for PNG with alpha)
#     pdf_buffer = io.BytesIO()
#     img_converted.save(pdf_buffer, format="PDF")
#     pdf_buffer.seek(0)
#     return pdf_buffer




def smart_merge(root_folder, output_name):
    master_merger = PyPDF2.PdfMerger()
    items = sorted(os.listdir(root_folder))
    
    # Supported formats
    image_exts = ('.png', '.jpg', '.jpeg', '.webp')
    
    for item in items:
        item_path = os.path.join(root_folder, item)
        
        # HANDLE FILES (PDF or Images)
        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()[1:]
            if item == output_name: continue
            
            if item.lower().endswith('.pdf'):
                print(f"Adding PDF: {item}")
                master_merger.append(item_path)
            elif item.lower().endswith(image_exts):
                print(f"Converting & Adding Image: {item}")
                img_pdf = convert_image_to_pdf(item_path)
                master_merger.append(img_pdf)
            

        # HANDLE FOLDERS
        elif os.path.isdir(item_path):
            print(f"Entering Folder: {item}")
            # Identify valid files
            sub_items = sorted([f for f in os.listdir(item_path) 
                               if f.lower().endswith(('.pdf', 'png', 'jpg', 'jpeg', 'webp'))])
            
            if sub_items:
                folder_merger = PyPDF2.PdfMerger()
                for s_item in sub_items:
                    s_path = os.path.join(item_path, s_item)
                    if s_item.lower().endswith('.pdf'):
                        folder_merger.append(s_path)
                    else:
                        folder_merger.append(convert_image_to_pdf(s_path))
                
                # --- FIX STARTS HERE ---
                # Instead of master_merger.append(folder_merger), 
                # we write the folder merger to a buffer first.
                temp_buffer = io.BytesIO()
                folder_merger.write(temp_buffer)
                folder_merger.close()
                temp_buffer.seek(0) # Go back to the start of the "file"
                
                master_merger.append(temp_buffer)
                # --- FIX ENDS HERE ---

        # # HANDLE FOLDERS
        # elif os.path.isdir(item_path):
        #     print(f"Entering Folder: {item}")
        #     sub_items = sorted([f for f in os.listdir(item_path) 
        #                        if f.lower().endswith(('.pdf',) + image_exts)])
            
        #     if sub_items:
        #         folder_merger = PyPDF2.PdfMerger()
        #         for s_item in sub_items:
        #             s_path = os.path.join(item_path, s_item)
        #             if s_item.lower().endswith('.pdf'):
        #                 folder_merger.append(s_path)
        #             else:
        #                 folder_merger.append(convert_image_to_pdf(s_path))
                
        #         master_merger.append(folder_merger)
        #         folder_merger.close()

    # Save
    output_path = os.path.join(root_folder, output_name)
    with open(output_path, "wb") as f:
        master_merger.write(f)
    master_merger.close()
    print(f"\nSuccess! Saved to: {output_path}")

def run_cli():
    parser = argparse.ArgumentParser(description="Deep merge PDFs and folders.")
    parser.add_argument("folder", nargs='?', default=".", help="Root folder path (default: current)")
    parser.add_argument("-o", "--output", default="Master_Combined.pdf", help="Output filename")
    
    args = parser.parse_args()
    smart_merge(args.folder, args.output)