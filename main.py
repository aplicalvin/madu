import tkinter as tk
from tkinter import messagebox
from navbar import create_sidebar  # Mengimpor sidebar/navbar dari navbar.py
from style import apply_styles
from PIL import Image, ImageTk  # Import PIL untuk menangani format gambar

# Fungsi untuk menampilkan halaman login
def login_window():
    def check_login():
        username = entry_username.get()
        password = entry_password.get()
        
        # Cek apakah username dan password sesuai
        if username == "admin" and password == "12345":
            root.destroy()  # Tutup jendela login
            main()  # Jalankan aplikasi utama
        else:
            # Tampilkan pesan kesalahan jika login gagal
            messagebox.showerror("Login Failed", "Username atau password salah!")
    
    # Halaman login
    root = tk.Tk()
    root.title("Login - Program Aplikasi Akuntansi")
    root.geometry("400x300")
    
    # Styling login
    apply_styles(root)  # Terapkan styling dari file style.py
    
    # Membuat frame untuk konten login
    frame_login = tk.Frame(root, bg="white", padx=20, pady=20)
    frame_login.pack(fill="both", expand=True)
    
    # Label dan input untuk username
    label_username = tk.Label(frame_login, text="Username", font=("Comic Sans MS", 14), bg="white")
    label_username.grid(row=0, column=0, pady=10, sticky="w")
    entry_username = tk.Entry(frame_login, font=("Comic Sans MS", 12))
    entry_username.grid(row=0, column=1, pady=10, sticky="w")
    
    # Label dan input untuk password
    label_password = tk.Label(frame_login, text="Password", font=("Comic Sans MS", 14), bg="white")
    label_password.grid(row=1, column=0, pady=10, sticky="w")
    entry_password = tk.Entry(frame_login, font=("Comic Sans MS", 12), show="*")
    entry_password.grid(row=1, column=1, pady=10, sticky="w")
    
    # Tombol untuk login
    button_login = tk.Button(frame_login, text="Login", font=("Comic Sans MS", 14), command=check_login)
    button_login.grid(row=2, columnspan=2, pady=20)
    
    # Menjalankan window login
    root.mainloop()

# Fungsi untuk aplikasi utama
def main():
    # GUI utama
    window = tk.Tk()
    window.title("Program Aplikasi Akuntansi")
    window.geometry("1280x720")

    # Terapkan styling dari file style.py
    apply_styles(window)

    # Frame utama untuk layout
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Frame konten utama (di kanan)
    frame_content = tk.Frame(window, bg="white")
    frame_content.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    # Menambahkan gambar latar belakang menggunakan canvas
    canvas_bg = tk.Canvas(frame_content, width=1280, height=720)
    canvas_bg.place(x=0, y=0)

    # Memuat gambar latar belakang menggunakan PIL
    bg_image = Image.open("assets/logo.jpg")  # Pastikan file gambar ada
    bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)

    # Konversi gambar PIL ke format Tkinter
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

# Menjalankan fungsi login terlebih dahulu sebelum aplikasi utama
login_window()
