import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from navbar import create_sidebar  # Mengimpor sidebar/navbar dari navbar.py
from jurnal import tambah_data, get_all_data, hitung_total  # Mengimpor logika jurnal dari jurnal.py
from style import apply_styles
from datetime import datetime

# Fungsi untuk menampilkan data dalam tabel
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)

    data = get_all_data()  # Mengambil data dari database melalui jurnal.py
    for row in data:
        tree.insert('', 'end', values=row[1:])  # Menampilkan semua data kecuali ID
    
    # Hitung total debit dan kredit
    total_debit, total_kredit = hitung_total()  # Menghitung total debit dan kredit
    label_total_debit.config(text=f"Total Debit: {total_debit}")
    label_total_kredit.config(text=f"Total Kredit: {total_kredit}")

# Fungsi untuk popup form input data
def popup_input_data():
    def simpan_data():
        tanggal = cal.get_date()
        no_produk = entry_no_produk.get()
        no_akun = entry_no_akun.get()
        nama_akun = entry_nama_akun.get()
        debet = entry_debet.get()
        kredit = entry_kredit.get()
        
        # Validasi input
        if not no_produk or not no_akun or not nama_akun or (not debet and not kredit):
            messagebox.showerror("Error", "Semua kolom harus diisi dengan benar!")
            return
        
        # Atur debet dan kredit secara otomatis
        debet = float(debet) if debet else 0
        kredit = float(kredit) if kredit else 0
        if debet > 0:
            kredit = 0
        if kredit > 0:
            debet = 0
        
        # Simpan data ke database
        tambah_data(tanggal, no_produk, no_akun, nama_akun, debet, kredit)
        tampilkan_data()  # Refresh tabel
        popup.destroy()
    
    # Popup untuk input data
    popup = tk.Toplevel(window)
    popup.title("Tambah Data Akuntansi")
    
    tk.Label(popup, text="Tanggal:").grid(row=0, column=0)
    cal = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.grid(row=0, column=1)
    cal.selection_set(datetime.today().date())  # Memilih tanggal default (hari ini)
    
    tk.Label(popup, text="No. Produk:").grid(row=1, column=0)
    entry_no_produk = tk.Entry(popup)
    entry_no_produk.grid(row=1, column=1)
    
    tk.Label(popup, text="No. Akun:").grid(row=2, column=0)
    entry_no_akun = tk.Entry(popup)
    entry_no_akun.grid(row=2, column=1)
    
    tk.Label(popup, text="Nama Akun:").grid(row=3, column=0)
    entry_nama_akun = tk.Entry(popup)
    entry_nama_akun.grid(row=3, column=1)
    
    tk.Label(popup, text="Debet:").grid(row=4, column=0)
    entry_debet = tk.Entry(popup)
    entry_debet.grid(row=4, column=1)
    
    tk.Label(popup, text="Kredit:").grid(row=5, column=0)
    entry_kredit = tk.Entry(popup)
    entry_kredit.grid(row=5, column=1)
    
    # Tombol untuk menyimpan data (gunakan ttk.Button untuk styling)
    ttk.Button(popup, text="Simpan", command=simpan_data, style="TButton").grid(row=6, columnspan=2)

# GUI utama
window = tk.Tk()
window.title("Program Aplikasi Akuntansi")
window.geometry("1200x600")

# Terapkan styling dari file style.py
apply_styles(window)

# Frame utama untuk layout (menggunakan grid untuk lebih fleksibel)
window.grid_rowconfigure(0, weight=1)  # Agar konten mengisi seluruh tinggi
window.grid_columnconfigure(1, weight=1)  # Kolom konten utama memiliki bobot lebih besar

# Frame konten utama (di kanan)
frame_content = tk.Frame(window, bg="white")
frame_content.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Membuat sidebar di kiri
current_page = "main"  # Set halaman default
create_sidebar(window, frame_content, current_page)

# Frame untuk konten utama
main_frame = tk.Frame(frame_content, bg="white")  # Frame utama di dalam frame_content
main_frame.pack(side="top", fill="both", expand=True)

# Label dan Tombol untuk Menambah Data
tk.Label(main_frame, text="Program Aplikasi Akuntansi", font=("Arial", 18), bg="sky blue").grid(row=0, column=0, pady=10)

# Ganti tk.Button dengan ttk.Button
ttk.Button(main_frame, text="Tambah Data", command=popup_input_data, style="TButton").grid(row=1, column=0, pady=10)

# Tabel untuk menampilkan data
columns = ("Tanggal", "No. Produk", "No. Akun", "Nama Akun", "Debet", "Kredit")
tree = ttk.Treeview(main_frame, columns=columns, show="headings", style="Treeview")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=2, column=0, pady=10)

# Ganti tk.Label dengan ttk.Label
label_total_debit = ttk.Label(main_frame, text="Total Debit: 0", style="TLabel")
label_total_debit.grid(row=3, column=0, pady=5)

label_total_kredit = ttk.Label(main_frame, text="Total Kredit: 0", style="TLabel")
label_total_kredit.grid(row=4, column=0, pady=5)

# Menampilkan data pertama kali
tampilkan_data()

# Menjalankan aplikasi
window.mainloop()
