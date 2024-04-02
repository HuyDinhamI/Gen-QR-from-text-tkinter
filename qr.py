import tkinter as tk
from tkinter import ttk
import cv2
import pyzbar.pyzbar as pyzbar
import qrcodegen  # Import the qrcodegen library
from PIL import Image, ImageTk
import io  # Import the io module for working with byte arrays

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng QR Code")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_generate_tab()
        self.create_scan_tab()

    def create_generate_tab(self):
        generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(generate_tab, text='Tạo QR')

        input_label = ttk.Label(generate_tab, text="Nhập văn bản:")
        input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.input_entry = ttk.Entry(generate_tab, width=30)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        generate_button = ttk.Button(generate_tab, text="Tạo QR", command=self.generate_qr)
        generate_button.grid(row=0, column=2, padx=5, pady=5)

        self.qr_label = ttk.Label(generate_tab, text="QR Code sẽ được hiển thị ở đây")
        self.qr_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def create_scan_tab(self):
        scan_tab = ttk.Frame(self.notebook)
        self.notebook.add(scan_tab, text='Quét QR')

        self.cam_label = ttk.Label(scan_tab, text="Ảnh từ Webcam")
        self.cam_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.canvas = tk.Canvas(scan_tab, width=640, height=480)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        scan_button = ttk.Button(scan_tab, text="Quét QR", command=self.scan_qr)
        scan_button.grid(row=2, column=0, padx=5, pady=5)

        back_button = ttk.Button(scan_tab, text="Quay lại", command=self.switch_to_generate_tab)
        back_button.grid(row=2, column=1, padx=5, pady=5)

        self.result_label = ttk.Label(scan_tab, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.capture = cv2.VideoCapture(0)
        self.update()

    def generate_qr(self):
        text = self.input_entry.get()
        if text:
            # Encode text into a QR code using qrcodegen library
            qr = qrcodegen.QrCode.encode_text(text, qrcodegen.QrCode.Ecc.QUARTILE)
            # Render the QR Code as a PNG image
            png_byte_array = qr.to_png(scale=20)
            # Create a PIL image from the PNG byte array
            img = Image.open(io.BytesIO(png_byte_array))
            img = ImageTk.PhotoImage(img)
            # Display the QR code image on the qr_label
            self.qr_label.config(image=img)
            self.qr_label.image = img

    def scan_qr(self):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = pyzbar.decode(gray)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                print("QR Code:", data)
                self.result_label.config(text="Thông tin QR Code: " + data)

    def switch_to_generate_tab(self):
        self.notebook.select(0)

    def update(self):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = pyzbar.decode(gray)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
       
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.image = img
            
        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
