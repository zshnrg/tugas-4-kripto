from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from lib.academic_db import Mahasiswa
from datetime import datetime
from pypdf import PdfReader

def create_transcript(mahasiswa: Mahasiswa = None):
    if mahasiswa:
        file_name = "[encrypted] " + mahasiswa.nim + "_transcript_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".pdf"
    else:
        file_name = "transcript.pdf"
        
    pdf = SimpleDocTemplate(file_name, pagesize=letter)
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
            TRANSKIP AKADEMIK<br/>
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
            """
            Nama : I Gusti Bagus Baskara<br/>
            NIM : 16520399<br/>
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
        ['1', 'II301', 'Matematika STI', '3', 'A'],
        ['2', 'II391', 'Manajemen Proyek', '2', 'AB'],
        # Tambahkan baris lain sesuai dengan kebutuhan
        ['10', 'II401', 'Tugas Akhir', '4', 'A']
    ]
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

    content.append(
        Paragraph(
            """
            <br/><br/><br/>
            Kepala Program Studi Sistem dan Teknologi Informasi<br/>
            <br/>
            --Begin signature--<br/>
            BFc65FFeCD2108CE340B<br/>
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

    pdf.build(content)

def read_transcript():
    try:
        pdf = PdfReader("transcript.pdf")
        raw = pdf.pages[0].extract_text()
        lines = raw.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        filtered = list(filter(lambda x: x != "", lines))

        print(filtered)

        # Extracting data from the transcript
        nim = filtered[5].split(": ")[1]
        nama = filtered[4].split(": ")[1]

        courses = []
        for i in range(filtered.index("No") + 5, filtered.index("A (4): Sangat baik, AB (3,5): Antara baik dan sangat baik, B (3): Baik, BC (2,5): Antara baik dan cukup, C (2):"), 5):
            courses.append({
                "kode": filtered[i+1],
                "nama": filtered[i+2],
                "sks": filtered[i+3],
                "nilai": filtered[i+4]
            })
        
        ipk = filtered[-6].split(": ")[1]
        sks = filtered[-7].split(": ")[1]
    except Exception as e:
        print("Error: PDF is invalid or corrupted")
        print(e)

    

if __name__ == "__main__":
    create_transcript()
    read_transcript()
