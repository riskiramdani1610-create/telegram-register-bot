"""
Database module untuk menyimpan data user dalam format TXT
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class UserDatabase:
    """Mengelola database user dalam file TXT"""
    
    def __init__(self, filename: str = "users.txt"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Memastikan file database ada"""
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()
    
    def _read_all_users(self) -> List[Dict]:
        """Membaca semua user dari file"""
        try:
            with open(self.filename, 'r') as f:
                users = []
                for line in f:
                    line = line.strip()
                    if line:
                        users.append(json.loads(line))
                return users
        except Exception as e:
            print(f"Error membaca database: {e}")
            return []
    
    def add_user(self, user_id: int, phone: str, name: str = None, 
                 status: str = "pending") -> bool:
        """Menambah user baru ke database"""
        try:
            # Cek apakah user sudah ada
            if self.get_user(user_id):
                return False
            
            user_data = {
                "user_id": user_id,
                "phone": phone,
                "name": name or "Unknown",
                "status": status,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            with open(self.filename, 'a') as f:
                f.write(json.dumps(user_data) + "\n")
            
            return True
        except Exception as e:
            print(f"Error menambah user: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Mendapatkan data user berdasarkan user_id"""
        users = self._read_all_users()
        for user in users:
            if user.get("user_id") == user_id:
                return user
        return None
    
    def get_user_by_phone(self, phone: str) -> Optional[Dict]:
        """Mendapatkan data user berdasarkan nomor HP"""
        users = self._read_all_users()
        for user in users:
            if user.get("phone") == phone:
                return user
        return None
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Update data user"""
        try:
            users = self._read_all_users()
            updated = False
            
            for user in users:
                if user.get("user_id") == user_id:
                    user.update(kwargs)
                    user["updated_at"] = datetime.now().isoformat()
                    updated = True
                    break
            
            if updated:
                self._write_users(users)
                return True
            return False
        except Exception as e:
            print(f"Error update user: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Menghapus user dari database"""
        try:
            users = self._read_all_users()
            users = [u for u in users if u.get("user_id") != user_id]
            self._write_users(users)
            return True
        except Exception as e:
            print(f"Error menghapus user: {e}")
            return False
    
    def _write_users(self, users: List[Dict]):
        """Menulis semua user ke file"""
        with open(self.filename, 'w') as f:
            for user in users:
                f.write(json.dumps(user) + "\n")
    
    def get_all_users(self) -> List[Dict]:
        """Mendapatkan semua user"""
        return self._read_all_users()


class SessionDatabase:
    """Mengelola session registrasi user"""
    
    def __init__(self, filename: str = "sessions.txt"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Memastikan file database ada"""
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()
    
    def _read_all_sessions(self) -> List[Dict]:
        """Membaca semua session dari file"""
        try:
            with open(self.filename, 'r') as f:
                sessions = []
                for line in f:
                    line = line.strip()
                    if line:
                        sessions.append(json.loads(line))
                return sessions
        except Exception as e:
            print(f"Error membaca session: {e}")
            return []
    
    def create_session(self, user_id: int, phone: str, step: str = "phone") -> str:
        """Membuat session baru untuk registrasi"""
        session_id = f"session_{user_id}_{int(datetime.now().timestamp())}"
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "phone": phone,
            "step": step,
            "otp_code": None,
            "verification_attempts": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            with open(self.filename, 'a') as f:
                f.write(json.dumps(session_data) + "\n")
            return session_id
        except Exception as e:
            print(f"Error membuat session: {e}")
            return None
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Mendapatkan session berdasarkan ID"""
        sessions = self._read_all_sessions()
        for session in sessions:
            if session.get("session_id") == session_id:
                return session
        return None
    
    def get_user_session(self, user_id: int) -> Optional[Dict]:
        """Mendapatkan session aktif user"""
        sessions = self._read_all_sessions()
        for session in sessions:
            if session.get("user_id") == user_id:
                return session
        return None
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session"""
        try:
            sessions = self._read_all_sessions()
            updated = False
            
            for session in sessions:
                if session.get("session_id") == session_id:
                    session.update(kwargs)
                    session["updated_at"] = datetime.now().isoformat()
                    updated = True
                    break
            
            if updated:
                self._write_sessions(sessions)
                return True
            return False
        except Exception as e:
            print(f"Error update session: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Menghapus session"""
        try:
            sessions = self._read_all_sessions()
            sessions = [s for s in sessions if s.get("session_id") != session_id]
            self._write_sessions(sessions)
            return True
        except Exception as e:
            print(f"Error menghapus session: {e}")
            return False
    
    def _write_sessions(self, sessions: List[Dict]):
        """Menulis semua session ke file"""
        with open(self.filename, 'w') as f:
            for session in sessions:
                f.write(json.dumps(session) + "\n")