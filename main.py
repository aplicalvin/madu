import tkinter as tk
from navbar import create_sidebar  # Mengimpor sidebar/navbar dari navbar.py
from style import apply_styles
from PIL import Image, ImageTk  # Import PIL untuk menangani format gambar

# GUI utama
window = tk.Tk()
window.title("Program Aplikasi Akuntansi")
window.geometry("1280x720")

# Terapkan styling dari file style.py (pastikan apply_styles di style.py juga menggunakan Comic Sans MS)
apply_styles(window)

# Frame utama untuk layout (menggunakan grid untuk lebih fleksibel)
window.grid_rowconfigure(0, weight=1)  # Agar konten mengisi seluruh tinggi
window.grid_columnconfigure(1, weight=1)  # Kolom konten utama memiliki bobot lebih besar

# Frame konten utama (di kanan)
frame_content = tk.Frame(window, bg="white")
frame_content.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Menambahkan gambar latar belakang menggunakan canvas
canvas_bg = tk.Canvas(frame_content, width=1280, height=720)
canvas_bg.place(x=0, y=0)

# Memuat gambar latar belakang menggunakan PIL
bg_image = Image.open("assets/logo.jpg")  # Pastikan file gambar ada
bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)  # Sesuaikan ukuran gambar dengan ukuran window

# Konversi gambar PIL ke format yang dapat diterima oleh Tkinter
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Tambahkan gambar ke canvas
canvas_bg.create_image(0, 0, image=bg_image_tk, anchor="nw")

# Membuat sidebar di kiri
current_page = "dashboard" 
create_sidebar(window, frame_content, current_page)

# Menambahkan header di bagian konten utama dengan font Comic Sans MS
header = tk.Label(frame_content, text="Sistea", font=("Comic Sans MS", 18, "bold"), bg="lightgreen", anchor="w", padx=20)
header.pack(fill="x", pady=10)

# Menjalankan aplikasi
window.mainloop()
