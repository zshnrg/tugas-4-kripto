
from supabase import create_client, Client
from postgrest.base_request_builder import APIResponse
from gotrue.types import AuthOtpResponse, AuthResponse

class Supabase():
    def __init__(self, public_key: str, url: str):
        self.public_key = public_key
        self.url = url
        self.client : Client = create_client(
            supabase_url=self.url,
            supabase_key=self.public_key
        )

    def getUser(self, email: str):
        # Get user from supabase
        data : APIResponse = self.client.table("users").select("*").eq("email", email).execute()
        if data.data == []:
            return None
        return data.data[0]

    def insertUser(self, email: str):
        # Insert user to supabase
        data : APIResponse = self.client.table("users").insert({"email": email}).execute()
        print(data)
        return data.data[0]

    def updateUser(self, email: str, data: dict):
        # Update user in supabase
        data : APIResponse = self.client.table("users").update(data).eq("email", email).execute()
        print(data)
        return data.data[0]
    
    def signUp(self, email: str):
        # Sign up user
        data : AuthOtpResponse = self.client.auth.sign_in_with_otp({
            "email": email
        })

    def verifyOTP(self, email: str, otp: str):
        # Verify OTP
        data : AuthOtpResponse = self.client.auth.verify_otp({
            "email": email,
            "token": otp,
            "type": "signup"
        })
        print(data)
        return data
    
    def getAcademic(self) -> list[dict]:
        # Get academic data
        data : APIResponse = self.client.table("view_academic").select("*").execute()
        if data.data == []:
            return None
        return data.data
    
    def getMahasiswa(self) -> list[dict]:
        # Get mahasiswa from supabase
        data : APIResponse = self.client.table("mahasiswa").select("*").execute()
        if data.data == []:
            return None
        return data.data
    
    def getMataKuliah(self) -> list[dict]:
        # Get mata kuliah from supabase
        data : APIResponse = self.client.table("courses").select("*").execute()
        if data.data == []:
            return None
        return data.data
    
    def getIndeks(self) -> list[dict]:
        # Get nilai from supabase
        data : APIResponse = self.client.table("grades").select("*").execute()
        if data.data == []:
            return None
        return data.data
    
    def getAllTranskrip(self) -> list[dict]:
        # Get transkrip from supabase
        data : APIResponse = self.client.table("transcript").select("*").execute()
        if data.data == []:
            return None
        return data.data
    
    def getTranskrip(self, nim: str) -> dict:
        # Get transkrip from supabase
        data : APIResponse = self.client.table("transcript").select("*").eq("nim", nim).execute()
        if data.data == []:
            return None
        return data.data[0]

    def insertMahasiswa(self, nim: str, nama: str):
        # Insert mahasiswa to supabase
        data : APIResponse = self.client.table("mahasiswa").insert({"nim": nim, "nama": nama}).execute()
        return data.data[0]
    
    def insertMataKuliah(self, kode: str, nama: str):
        # Insert mata kuliah to supabase
        data : APIResponse = self.client.table("courses").insert({"kode": kode, "nama": nama}).execute()
        return data.data[0]
        
    def insertIndeks(self, nim: str, kode: str, indeks: str):
        # Insert nilai to supabase
        data : APIResponse = self.client.table("grades").insert({"nim": nim, "kode_mata_kuliah": kode, "indeks": indeks}).execute()
        return data.data[0]
    
    def insertTranskrip(self, nim: str, signature: str, public_key: str):
        # Insert transkrip to supabase
        data : APIResponse = self.client.table("transcript").insert({"nim": nim, "signature": signature, "public_key": public_key}).execute()
        return data.data[0]
    
    def updateTranskrip(self, nim: str, signature: str, public_key: str):
        # Update transkrip in supabase
        data : APIResponse = self.client.table("transcript").update({"signature": signature, "public_key": public_key}).eq("nim", nim).execute()
        return data.data[0]
    
    def deleteTranskrip(self, nim: str):
        # Delete transkrip from supabase
        data : APIResponse = self.client.table("transcript").delete().eq("nim", nim).execute()
        return data.data[0]
        

supabase_url = 'https://jtzydbpyjtramwqmdeyv.supabase.co'
public_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp0enlkYnB5anRyYW13cW1kZXl2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTUyOTQ1ODcsImV4cCI6MjAzMDg3MDU4N30.FS1ogrI75GfiY1wQgNu_En6AB2WHdKwa2479sK8OZhY'

db = Supabase(public_key, supabase_url)
db.getUser("baskara@itb.ac.id")