from flet import *
from services.db import Supabase
from lib.cipher.modifiedRC4 import RC4
import base64

class Course():
    def __init__(self, kode: str, nama: str, sks: int):
        self.kode = kode
        self.nama = nama
        self.sks = sks

    def encrypt(self, key: str):
        rc4 = RC4(key)
        self.kode = base64.b64encode(rc4.encrypt(self.kode.encode())).decode()
        self.nama = base64.b64encode(rc4.encrypt(self.nama.encode())).decode()
        self.sks = base64.b64encode(rc4.encrypt(str(self.sks).encode())).decode()

    def decrypt(self, key: str):
        rc4 = RC4(key)
        self.kode = rc4.decrypt(base64.b64decode(self.kode)).decode()
        self.nama = rc4.decrypt(base64.b64decode(self.nama)).decode()
        self.sks = int(rc4.decrypt(base64.b64decode(self.sks)).decode())
        
class TakenCourse():
    def __init__(self, course: Course, indeks: str):
        self.course = course
        self.indeks = indeks

    def encrypt(self, key: str):
        self.course.encrypt(key)
        rc4 = RC4(key)
        self.indeks = base64.b64encode(rc4.encrypt(self.indeks.encode())).decode()

    def decrypt(self, key: str):
        self.course.decrypt(key)
        rc4 = RC4(key)
        self.indeks = rc4.decrypt(base64.b64decode(self.indeks)).decode()

class Mahasiswa():
    def __init__(self, nim: str, nama: str, ipk: float = 0, signature: str = None):
        self.nim = nim
        self.nama = nama
        self.mata_kuliah : list[TakenCourse] = []
        self.ipk = ipk
        self.signature = signature

    def add_course(self, course: TakenCourse):
        self.mata_kuliah.append(course)
        self.calculate_ipk()

    def remove_course(self, course: TakenCourse):
        self.mata_kuliah.remove(course)

    def calculate_ipk(self):
        total_sks = 0
        total_bobot = 0
        for mk in self.mata_kuliah:
            total_sks += mk.course.sks
            total_bobot += mk.course.sks * self._nilai_to_bobot(mk.indeks)

    def _nilai_to_bobot(self, nilai: str):
        if nilai == "A":
            return 4
        elif nilai == "AB":
            return 3.5
        elif nilai == "B":
            return 3
        elif nilai == "BC":
            return 2.5
        elif nilai == "C":
            return 2
        elif nilai == "D":
            return 1
        elif nilai == "E":
            return 0

    def to_dict(self):
        data = {
            "nim": self.nim,
            "nama_mahasiswa": self.nama,
            "mata_kuliah": [],
            "ipk": self.ipk
        }
        for mk in self.mata_kuliah:
            data["mata_kuliah"].append({
                "kode": mk.course.kode,
                "nama": mk.course.nama,
                "sks": mk.course.sks,
                "nilai": mk.indeks
            })
        return data
    
    @staticmethod
    def from_dict(data: dict):
        mahasiswa = Mahasiswa(data["nim"], data["nama_mahasiswa"], data["ipk"])
        for mk in data["mata_kuliah"]:
            mahasiswa.add_course(TakenCourse(Course(mk["kode"], mk["nama"], mk["sks"]), mk["nilai"]))
        return mahasiswa
    
    def encrypt(self, key: str):
        rc4 = RC4(key)
        self.nim = base64.b64encode(rc4.encrypt(self.nim.encode())).decode()
        self.nama = base64.b64encode(rc4.encrypt(self.nama.encode())).decode()
        self.ipk = base64.b64encode(rc4.encrypt(str(self.ipk).encode())).decode()
        for mk in self.mata_kuliah:
            mk.encrypt(key)
        if self.signature is not None:
            self.signature = base64.b64encode(rc4.encrypt(self.signature.encode())).decode()

    def decrypt(self, key: str):
        rc4 = RC4(key)
        self.nim = rc4.decrypt(base64.b64decode(self.nim)).decode()
        self.nama = rc4.decrypt(base64.b64decode(self.nama)).decode()
        self.ipk = float(rc4.decrypt(base64.b64decode(self.ipk)).decode())
        for mk in self.mata_kuliah:
            mk.decrypt(key)
        if self.signature is not None:
            self.signature = rc4.decrypt(base64.b64decode(self.signature)).decode()


class AcademicData():
    def __init__(self, page: Page, database: Supabase):
        self.page = page
        self.database = database
        self.mahasiswa : list[Mahasiswa] = []
        self.available_mata_kuliah : list[Course] = []
        self.is_encrypted = False

    def load(self):
        self.mahasiswa = self.page.client_storage.get("database.academic_data")
        self.is_encrypted = self.page.client_storage.get("database.is_encrypted")

    def save(self):
        # asyncio.create_task(
        #     self._save_async()
        # )

        self.page.client_storage.set("database.academic_data", self.mahasiswa)
        self.page.client_storage.set("database.is_encrypted", self.is_encrypted)

    async def _save_async(self):
        await self.page.client_storage.set_async("database.academic_data", self.mahasiswa)
        await self.page.client_storage.set_async("database.is_encrypted", self.is_encrypted)

    def load_from_db(self):
        self.mahasiswa = []
        self.available_mata_kuliah = []
        data = self.database.getAcademic()
        if data is None:
            return
        for d in data:
            mahasiswa = Mahasiswa(d["nim"], d["nama_mahasiswa"], d["ipk"], d["signature"])
            self.mahasiswa.append(mahasiswa)
            # Split mata kuliah
            kode_mk = d["kode_mata_kuliah"].split(", ")
            nama_mk = d["nama_mata_kuliah"].split(", ")
            sks = d["sks"].split(", ")
            indeks = d["indeks"].split(", ")
            for i in range(len(kode_mk)):
                # check if course already exists, if not add it to available_mata_kuliah
                course = Course(kode_mk[i], nama_mk[i], int(sks[i]))
                if course not in self.available_mata_kuliah:
                    self.available_mata_kuliah.append(course)

                # add course to mahasiswa
                mahasiswa.add_course(TakenCourse(course, indeks[i]))

        if self.is_encrypted:
            self.encrypt(self.page.key)

    def save_to_db(self):
        if self.is_encrypted:
            self.decrypt(self.page.key)
        
        # load data from online database, and compare it with local data to determine which data to insert on the online database
        mahasiswa = self.database.getMahasiswa()
        all_nim = [m["nim"] for m in mahasiswa]
        for m in self.mahasiswa:
            if m.nim not in all_nim:
                self.database.insertMahasiswa(m.nim, m.nama)
        mata_kuliah = self.database.getMataKuliah()
        all_kode = [m["kode"] for m in mata_kuliah]
        for mk in m.mata_kuliah:
            if mk.course.kode not in all_kode:
                self.database.insertMataKuliah(mk.course.kode, mk.course.nama)
        nilai = self.database.getIndeks()
        for m in self.mahasiswa:
            for mk in m.mata_kuliah:
                for n in nilai:
                    if n["nim"] == m.nim and n["kode_mata_kuliah"] == mk.course.kode:
                        break
                else:
                    self.database.insertIndeks(m.nim, mk.course.kode, mk.indeks)

        transkrip = self.database.getAllTranskrip()
        for m in self.mahasiswa:
            # check if signature is already in the database for mahasiswa with signature is not None
            if m.signature is not None:
                if {"nim": m.nim, "signature": m.signature} not in transkrip:
                    self.database.insertTranskrip(m.nim, m.signature)

    def add_mahasiswa(self, mahasiswa: Mahasiswa):
        if self.is_encrypted:
            mahasiswa.encrypt(self.page.key)
        self.mahasiswa.append(mahasiswa)
        self.save()

    def get_mahasiswa(self, nim: str):
        if self.is_encrypted:
            self.decrypt(self.page.key)
        for m in self.mahasiswa:
            if m.nim == nim:
                return m
        return None
    
    def get_course(self, kode: str):
        if self.is_encrypted:
            self.decrypt(self.page.key)
        for c in self.available_mata_kuliah:
            if c.kode == kode:
                return c
        return None
    
    def add_course_grade(self, nim: str, course: TakenCourse):
        if self.is_encrypted:
            self.decrypt(self.page.key)
        m = self.get_mahasiswa(nim)
        if m is not None:
            m.add_course(course)
            self.save()

    def add_course(self, course: Course):
        if self.is_encrypted:
            course.encrypt(self.page.key)
        self.available_mata_kuliah.append(course)
        self.save()

    def add_signature(self, nim: str, signature: str):
        if self.is_encrypted:
            self.decrypt(self.page.key)
        m = self.get_mahasiswa(nim)
        if m is not None:
            m.signature = signature
            self.save()

    def to_dict(self):
        data = []
        for d in self.mahasiswa:
            data.append(d.to_dict())
        return data
    
    @staticmethod
    def from_dict(data: list[dict]):
        academic_data = AcademicData()
        for d in data:
            academic_data.add_mahasiswa(Mahasiswa.from_dict(d))
        return academic_data
    
    def encrypt(self, key: str):
        if self.is_encrypted:
            return
        for m in self.mahasiswa:
            m.encrypt(key)
        self.is_encrypted = True
        print("Encrypted")

    def decrypt(self, key: str):
        if not self.is_encrypted:
            return
        for m in self.mahasiswa:
            m.decrypt(key)
        self.is_encrypted = False
        print("Decrypted")