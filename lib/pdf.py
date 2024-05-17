from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle, TA_CENTER

from pypdf import PdfReader
from io import BytesIO
import base64

from lib.academic_db import Mahasiswa
from lib.cipher.rsa import RSA
from lib.cipher.sha import Keccak

def create_transcript(
    mahasiswa: Mahasiswa = None, 
    public_key: str = None,
    ):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    content = []

    content.append(
        Paragraph(
            """
            INSTITUT TEKNOLOGI BANDUNG<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Bold',
                fontSize=20,
                alignment=TA_CENTER,
                spaceAfter=10
            )
        )
    )

    content.append(
        Paragraph(
            """
            SEKOLAH TEKNIK ELEKTRO DAN INFORMATIKA<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Bold',
                fontSize=14,
                alignment=TA_CENTER,
                spaceAfter=5
            )
        )
    )

    content.append(
        Paragraph(
            """
            PROGRAM STUDI SISTEM DAN TEKNOLOGI INFORMASI<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Bold',
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=8
            )
        )
    )

    content.append(
        Paragraph(
            """
            Jalan Ganesha 10 Bandung 40132 Telp. (022) 2502260, (022) 4254028 Fax. (022) 2534222<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Roman',
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=8
            )
        )
    )

    content.append(
        HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black)
    )

    content.append(
        Paragraph(
            """
            <br/>
            TRANSKRIP AKADEMIK<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Bold',
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=10
            )
        )
    )

    content.append(
        Paragraph(
            f"""
            Nama : {mahasiswa.nama}<br/>
            NIM : {mahasiswa.nim}<br/>
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Roman',
                fontSize=12,
                leading=14,
                spaceAfter=14
            )
        )
    )

    data = [
        ['No', 'Kode Mata Kuliah', 'Nama Mata Kuliah', 'SKS', 'Nilai'],
    ]

    if mahasiswa:
        oneline_data = mahasiswa.nim + mahasiswa.nama
        index = 1
        for mk in mahasiswa.mata_kuliah:
            data.append([
                str(index),
                mk.course.kode,
                mk.course.nama,
                str(mk.course.sks),
                mk.indeks
            ])
            oneline_data += mk.course.kode + mk.course.nama + str(mk.course.sks) + mk.indeks
            index += 1



    table = Table(data, colWidths=[40, 100, 240, 40, 40])

    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    content.append(table)
    content.append(
        Paragraph("<br/><br/>")
    )

    content.append(
        HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black)
    )

    content.append(
        Paragraph(
            "<br/>A (4): Sangat baik, AB (3,5): Antara baik dan sangat baik, B (3): Baik, BC (2,5): Antara baik dan cukup, C (2): Cukup, D (1): Kurang atau hampir cukup",
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Roman',
                fontSize=10,
                leading=14,
                spaceAfter=14
            )
        )
    )

    content.append(
        HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black)
    )

    content.append(
        Table(
            [
                ['Total SKS : 22', 'IPK : 3.75']
            ],
            colWidths=[230, 230],
            style=TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
            ])
        )
    )

    sha = Keccak()
    oneline_data_hash = sha.hash(oneline_data.encode())
    oneline_data_base64 = base64.b64encode(oneline_data_hash).decode()

    rsa = RSA()
    rsa.set_keys(public_key=public_key)
    encrypted_data = rsa.encrypt(oneline_data_base64)

    numbers_str = [str(num) for num in encrypted_data]
    numbers_concat = ",".join(numbers_str)
    signature = base64.b64encode(numbers_concat.encode()).decode()

    content.append(
        Paragraph(
            f"""
            <br/><br/><br/>
            Kepala Program Studi Sistem dan Teknologi Informasi<br/>
            <br/>
            --Begin signature--<br/>
            {signature}<br/>
            --End signature--<br/><br/>
            (Dr. I Gusti Bagus Baskara)
            """,
            style=ParagraphStyle(
                name='HeaderCustomStyle',
                fontName='Times-Roman',
                fontSize=12,
                leading=14,
                spaceAfter=14
            )
        )
    )

    doc.build(content)
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data, signature

def read_transcript(path : str):
    try:
        pdf = PdfReader(path)
        raw = pdf.pages[0].extract_text()
        lines = raw.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        filtered = list(filter(lambda x: x != "", lines))

        print(filtered)

        # Extracting data from the transcript
        header_index = filtered.index("TRANSKRIP AKADEMIK")
        nim = filtered[header_index + 2].split(": ")[1]
        nama = filtered[header_index + 1].split(": ")[1]

        print(nim, nama)

        courses = []
        if "No" not in filtered:
            return "Edit detected"
        else:
            for i in range(filtered.index("No") + 5, filtered.index("A (4): Sangat baik, AB (3,5): Antara baik dan sangat baik, B (3): Baik, BC (2,5): Antara baik dan cukup, C (2):"), 5):
                courses.append({
                    "kode": filtered[i+1],
                    "nama": filtered[i+2],
                    "sks": filtered[i+3],
                    "nilai": filtered[i+4]
                })

        print(courses)

        sign_header_index = filtered.index("Kepala Program Studi Sistem dan Teknologi Informasi")
        
        ipk = filtered[sign_header_index - 1].split(": ")[1]
        sks = filtered[sign_header_index - 2].split(": ")[1]

        print(ipk, sks)

        oneline_data = nim + nama
        for course in courses:
            oneline_data += course["kode"] + course["nama"] + course["sks"] + course["nilai"]
        
        sha = Keccak()
        oneline_data_hash = sha.hash(oneline_data.encode())
        oneline_data_base64 = base64.b64encode(oneline_data_hash).decode()

        signature_begin = filtered.index("--Begin signature--")
        signature_end = filtered.index("--End signature--")

        signature = ''.join(filtered[signature_begin+1:signature_end])

        print("Read signature:\n", signature)

        return nim, oneline_data_base64, signature

    except Exception as e:
        print("Error: PDF is invalid or corrupted")
        return None, None, None

    

if __name__ == "__main__":
    create_transcript()
    read_transcript()
