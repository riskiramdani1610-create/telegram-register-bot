# API Client untuk komunikasi dengan h5.bigwinner10.com
import requests
import json
import hashlib
from config import *
from utils.sign_generator import generate_timestamp

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = API_BASE_URL
        self.user_id = None
        self.auth_token = None
        self.phone = None
    
    def _get_headers(self):
        """Generate headers untuk request"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Android)',
        }
        
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        return headers
    
    def _make_request(self, method, endpoint, payload=None, sign=None):
        """
        Buat request ke API
        CATATAN: Sign parameter masih perlu di-handle dengan benar
        """
        url = f"{self.base_url}{endpoint}"
        
        if sign:
            url += f"?sign={sign}"
        
        headers = self._get_headers()
        
        try:
            if method == 'POST':
                response = self.session.post(url, json=payload, headers=headers)
            else:
                response = self.session.get(url, headers=headers)
            
            return response.status_code, response.json()
        except Exception as e:
            print(f"Request error: {e}")
            return None, str(e)
    
    def bind_custom_account(self, phone_number, password, sign):
        """
        Step 1: Bind akun dengan nomor acak
        
        Args:
            phone_number: Nomor telepon acak (bisa apa saja)
            password: Password
            sign: Sign parameter (dari frontend)
        
        Returns:
            status_code, response
        """
        payload = {
            "phone": phone_number,
            "password": password,
            "header": {
                "timestamp": generate_timestamp()
            }
        }
        
        status, response = self._make_request('POST', '/bind/custom-account', payload, sign)
        
        if status == 200:
            # Simpan info untuk request berikutnya
            if 'header' in response:
                self.user_id = response['header'].get('userId')
                self.auth_token = response['header'].get('token')
        
        return status, response
    
    def request_otp(self, phone_number, sign):
        """
        Step 2: Request OTP ke nomor asli
        
        Args:
            phone_number: Nomor telepon ASLI
            sign: Sign parameter
        
        Returns:
            status_code, response
        """
        payload = {
            "phone": phone_number,
            "verifyCode": "",  # Kosong saat request OTP
            "autoReceiveReward": True,
            "header": {
                "timestamp": generate_timestamp(),
                "userId": self.user_id,
                "authToken": self.auth_token
            }
        }
        
        status, response = self._make_request('POST', '/bind/phone', payload, sign)
        
        if status == 200:
            self.phone = phone_number
        
        return status, response
    
    def verify_otp(self, phone_number, otp_code, sign):
        """
        Step 3: Verifikasi OTP
        
        Args:
            phone_number: Nomor telepon ASLI
            otp_code: OTP dari SMS
            sign: Sign parameter
        
        Returns:
            status_code, response
        """
        payload = {
            "phone": phone_number,
            "verifyCode": otp_code,
            "autoReceiveReward": True,
            "header": {
                "timestamp": generate_timestamp(),
                "userId": self.user_id,
                "authToken": self.auth_token
            }
        }
        
        status, response = self._make_request('POST', '/bind/phone', payload, sign)
        
        return status, response
