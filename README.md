# XIS - Sistem Informasi Akademik

<center>

  ![alt text](/assets/icon.png "XIS Icon")
</center>
  
<p align="center">
Tugas 4 II44031 Kriptografi dan Koding : Implementasi Basis Data Terenkripsi dan Bertanda-tangan Digital dengan Menggunakan Algoritma RSA dan Fungsi Hash SHA-3
</p>

<p align="center">
18221121 Natasya Vercelly Harijadi - 18221121 Rozan Ghosani
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#system-requirement">System Requirements</a> |
  <a href="#how-to-run">How to Run</a> |
  <a href="#apk-installation">APK Installation (Coming Soon)</a> |
  <a href="#features">Features</a>
</p>

## About
Program ini merupakan program yang mengimplementasi tanda tangan digital menggunakan algoritma RSA dan SHA-3 (Keccak). Studi kasus yang digunakan adalah database akademik berisi data mahasiswa, mata kuliah yang diambil, bobot SKS untuk mata kuliah tersebut, dan indeks setiap mata kuliah. Program juga dapat menghitung Indeks Prestasi Kumulatif (IPK) dari setiap mahasiswa secara otomatis. Program dapat mengenkripsi dan mendekripsi seluruh field pada database akademik. 

## System Requirement

- Python 3.8 atau lebih baru.
- Library Flet versi terbaru
- Flutter SDK 3.16 atau lebih baru (apabila ingin melakukan build)
- Developer mode pada Windows 11
- Visual Studio Code

## How to Run
### Cloning repository
1. Pada halaman utama repository [GitHub](https://github.com/zshnrg/tugas-4-kripto), buka menu **Clone** lalu salin URL dari repository
2. Buka Terminal
3. Pindah ke direktori yang diinginkan
4. Ketikan `git clone`, lalu tempelkan URL yang telah disalin tadi 
   ```sh
   git clone https://github.com/zshnrg/tugas-4-kripto.git
   ```

### Running the app
1. Pindah ke directory `tugas-4-kripto`
2. Install depedencies yang diperlukan
   ```sh
   pip install -r requirements.txt
   ```
3. Jalankan app dengan cara 
    Aplikasi dijalankan di komputer secara langsung
    ```sh
    flet run
    ```

### Installation - Windows

1. Lihat rilis terbaru aplikasi ini di [GitHub](https://github.com/zshnrg/tugas-4-kripto/releases)
2. Unduh aplikasi dengan ekstensi `.exe`
3. Install aplikasi yang telah diunduh

### Building it Instead
Saat ini aplikasi XIS hanya dibuat kompatibel sebagai aplikasi desktop di Windows. Untuk melakukan build pastikan requirements berikut ini sudah terinstall:

- Library Flet versi terbaru
- Flutter (Channel stable, 3.19.6, on Microsoft Windows [Version 10.0.19045.4291], locale en-US)
- Windows Version (Installed version of Windows is version 10 or higher)
- Android toolchain - develop for Android devices (Android SDK version 34.0.0)
- Chrome - develop for the web
- Visual Studio - develop Windows apps (Visual Studio Community 2022 17.9.7)
- Android Studio (version 2023.3)
- VS Code (version 1.89.1)

Kemudian jalankan perintah berikut ini pada terminal di direktori `tugas-4-kripto/`

```sh
flet build windows
```

Tunggu 5-20 menit hingga aplikasi telah berhasil di-build

```
Creating Flutter bootstrap project...OK
Customizing app icons and splash images...OK
Generating app icons...OK
Packaging Python app...OK
Building Windows app...OK
Copying build to build\windows directory...OK
Success!
```

## Features
Program ini memiliki fitur:
- Login dan pendaftaran akun
- Pemilihan role mahasiswa atau dosen
- Database akademik mahasiswa yang dienkripsi dengan tanda tangan digital
- Pembuatan transkrip mahasiswa yang dienkripsi dengan tanda tangan digital