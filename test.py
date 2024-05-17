# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import io

# def create_pdf_in_memory():
#     # Membuat buffer di memori
#     buffer = io.BytesIO()

#     # Membuat canvas untuk PDF
#     c = canvas.Canvas(buffer, pagesize=letter)
#     c.drawString(100, 750, "Hello World")
#     c.save()

#     # Dapatkan data PDF dari buffer
#     pdf_data = buffer.getvalue()
#     buffer.close()
    
#     return pdf_data

# def simple_encrypt(data, key):
#     # Fungsi enkripsi sederhana (contoh XOR enkripsi)
#     encrypted_data = bytearray()
#     for i in range(len(data)):
#         encrypted_data.append(data[i] ^ key)
#     return bytes(encrypted_data)

# def save_encrypted_pdf(pdf_data, key, filename):
#     # Enkripsi data PDF
#     encrypted_data = simple_encrypt(pdf_data, key)

#     # Simpan data terenkripsi ke dalam file
#     with open(filename, 'wb') as f:
#         f.write(encrypted_data)

# def load_and_decrypt_pdf(filename, key):
#     # Membaca data terenkripsi dari file
#     with open(filename, 'rb') as f:
#         encrypted_data = f.read()

#     # Dekripsi data PDF
#     decrypted_data = simple_encrypt(encrypted_data, key)
    
#     return decrypted_data

# def save_pdf_to_file(pdf_data, filename):
#     # Menyimpan data PDF yang didekripsi ke dalam file
#     with open(filename, 'wb') as f:
#         f.write(pdf_data)

# # Membuat PDF dalam memori
# pdf_data = create_pdf_in_memory()

# # Kunci enkripsi (misalnya 0x42)
# key = 0x42

# # Nama file output terenkripsi
# encrypted_filename = 'encrypted_document.pdf'

# # Menyimpan PDF terenkripsi
# save_encrypted_pdf(pdf_data, key, encrypted_filename)
# print(f"File terenkripsi disimpan sebagai {encrypted_filename}")

# # Mendekripsi file yang telah terenkripsi
# decrypted_pdf_data = load_and_decrypt_pdf(encrypted_filename, key)

# # Nama file output didekripsi
# decrypted_filename = 'decrypted_document.pdf'

# # Menyimpan PDF yang telah didekripsi
# save_pdf_to_file(decrypted_pdf_data, decrypted_filename)
# print(f"File didekripsi disimpan sebagai {decrypted_filename}")


with open("[encrypted] 18221121_transcript_20240516120905.pdf", "rb") as f:
    data = f.read()

    print(data[:100])