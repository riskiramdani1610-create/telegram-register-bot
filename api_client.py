"""
API Client untuk Pangtiger
"""
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class PangtierAPIClient:
    """Client untuk berkomunikasi dengan Pangtiger API"""
    
    def __init__(self, base_url: str = "https://api.pangtiger.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TelegramRegistrationBot/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """Membuat HTTP request ke API"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, params=params, timeout=10)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported HTTP method: {method}"
                }
            
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json() if response.text else {},
                "status_code": response.status_code
            }
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout saat mengakses {endpoint}")
            return {
                "success": False,
                "error": "Request timeout",
                "status_code": 408
            }
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error ke {endpoint}")
            return {
                "success": False,
                "error": "Connection error",
                "status_code": 0
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": e.response.status_code if e.response else 0
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 0
            }
    
    def register_phone(self, phone: str) -> Dict[str, Any]:
        """
        Registrasi nomor HP
        Endpoint: POST /api/user/phone_register
        """
        data = {
            "phone": phone
        }
        return self._make_request("POST", "/api/user/phone_register", data=data)
    
    def verify_code(self, phone: str, code: str) -> Dict[str, Any]:
        """
        Verifikasi kode OTP
        Endpoint: POST /userverse/api/v1/verify-code/user/phone
        """
        data = {
            "phone": phone,
            "code": code
        }
        return self._make_request("POST", "/userverse/api/v1/verify-code/user/phone", data=data)
    
    def bind_custom_account(self, user_id: str, custom_account: str, 
                           password: str) -> Dict[str, Any]:
        """
        Bind custom account ke user
        Endpoint: POST /hall/userverse/api/v1/bind/custom-account
        """
        data = {
            "user_id": user_id,
            "custom_account": custom_account,
            "password": password
        }
        return self._make_request("POST", "/hall/userverse/api/v1/bind/custom-account", data=data)
    
    def health_check(self) -> bool:
        """Cek koneksi ke API"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            return response.status_code < 500
        except:
            return False