import os
import fitz
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog

class PDFtoImageConverter:

    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Image Converter")
        
        self.pdf_files = []

        self.format_var = StringVar(value="JPG")
        ttk.Label(root, text="Output Format").pack(pady=5)

        ttk.Combobox(
        root,
        textvariable=self.format_var,
        values=["JPG", "PNG"],
        state="readonly"    
        ).pack()
        

        #convert button
        ttk.Button(
            root,
            text="Select PDFs",
            command=self.select_files
        ).pack(pady=10)

        #convert button
        ttk.Button(
            root,
            text="Convert PDFs",
            command=self.convert_files
        ).pack(pady=10)

        #status box
        self.status = Text(root, height=10)
        self.status.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message):

        self.status.insert(END, message + "\n")
        self.status.see(END)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        self.pdf_files = list(files)
        self.log(f"Loaded {len(self.pdf_files)} PDF file(s)")

    def drop_files(self, event):

        files = self.root.tk.splitlist(event.data)

        self.pdf_files = [
            f for f in files
            if f.lower().endswith(".pdf")
        ]

        self.log(f"Loaded {len(self.pdf_files)} PDF file(s)"
                )
    def convert_files(self):
        if not self.pdf_files:
            messagebox.showwarning(
                "No Files",
                "Please select one or more PDF files."


            )
            return
        
        selected_format = self.format_var.get()

        for pdf_path in self.pdf_files:
            try:
                pdf_name = os.path.splitext(
                    os.path.basename(pdf_path)
                )[0]

                output_folder = os.path.join(
                    os.path.dirname(pdf_path),
                    pdf_name + "_Images"
                )

                os.makedirs(output_folder, exist_ok=True)

                self.log(f"Processing {pdf_name}")

                pdf = fitz.open(pdf_path)

                for page_num in range(len(pdf)):
                    page = pdf[page_num]

                    zoom = 3
                    matrix = fitz.Matrix(zoom, zoom)

                    pix = page.get_pixmap(matrix=matrix)

                    if selected_format == "PNG":
                        output_file = os.path.join(
                            output_folder, f"{pdf_name}_page{page_num+1}.png"
                        )

                        pix.save(output_file)
                    else:
                        output_file = os.path.join(
                            output_folder, 
                            f"{pdf_name}_page{page_num+1}.jpg"
                        )
                        pix.save(output_file)
                    self.log(
                        f"Saved Page {page_num+1}"
                    
                    )
                pdf.close()

            except Exception as e:
                self.log(
                    f"Error processing {pdf_path}: {e}"
                )
        messagebox.showinfo(
            "Complete",
            "Conversion finished."
        )
root = Tk()
app = PDFtoImageConverter(root)
root.mainloop()


