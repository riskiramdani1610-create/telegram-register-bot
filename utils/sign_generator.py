# Sign Generator - untuk generate sign parameter
import hashlib
import json
import time

def generate_sign(data_dict):
    """
    Generate sign parameter untuk API request.
    CATATAN: Ini temporary - tunggu kita find algoritma yang tepat!
    
    Sekarang cuma placeholder, nanti di-update pas ketemu pattern-nya
    """
    try:
        # Coba berbagai kombinasi
        phone = data_dict.get('phone', '')
        verify_code = data_dict.get('verifyCode', '')
        timestamp = data_dict.get('header', {}).get('timestamp', '')
        
        # Placeholder - akan di-update
        # Untuk sekarang, return None dan handle di request function
        return None
    except Exception as e:
        print(f"Error generating sign: {e}")
        return None

def generate_timestamp():
    """Generate current timestamp dalam milliseconds"""
    return int(time.time() * 1000)
