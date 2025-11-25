"""
Database Handler
----------------
Simple SQLite wrapper to save user data and history.
Nothing fancy, just basic CRUD operations.
"""

import sqlite3
import os
from datetime import datetime
import json


class DatabaseManager:
    def __init__(self, db_path='data/users.db'):
        self.db_path = db_path
        # Make sure the folder exists!
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _get_conn(self):
        """Quick helper to get a connection"""
        return sqlite3.connect(self.db_path)
    
    def _init_db(self):
        """Sets up the tables if they don't exist"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            # Table for users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Table for history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    num_faces INTEGER,
                    emotions_detected TEXT,
                    average_confidence REAL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Table for stats
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotion_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    emotion TEXT,
                    count INTEGER DEFAULT 1,
                    last_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Database ready!")
            
        except Exception as e:
            print(f"DB Init failed: {e}")
    
    def create_user(self, username, email=None):
        """Adds a new user to the db"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, created_at)
                VALUES (?, ?, ?)
            ''', (username, email, datetime.now()))
            
            uid = cursor.lastrowid
            conn.commit()
            conn.close()
            return uid
            
        except sqlite3.IntegrityError:
            # User probably already exists, just get their ID
            return self.get_user_by_username(username)['id']
        except Exception as e:
            print(f"Could not create user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Finds a user by their name"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, created_at, last_login
                FROM users
                WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'created_at': row[3],
                    'last_login': row[4]
                }
            return None
            
        except Exception as e:
            print(f"User lookup failed: {e}")
            return None
    
    def update_last_login(self, user_id):
        """Updates the last login timestamp"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Login update failed: {e}")
    
    def save_detection_history(self, user_id, num_faces, emotions, avg_conf):
        """Logs a detection event"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            # JSON dump the list because SQLite doesn't have arrays
            emo_json = json.dumps(emotions)
            
            cursor.execute('''
                INSERT INTO detection_history 
                (user_id, num_faces, emotions_detected, average_confidence)
                VALUES (?, ?, ?, ?)
            ''', (user_id, num_faces, emo_json, avg_conf))
            
            hid = cursor.lastrowid
            
            # Also update the aggregate stats
            for emo in emotions:
                self._update_stats(cursor, user_id, emo)
            
            conn.commit()
            conn.close()
            return hid
            
        except Exception as e:
            print(f"History save failed: {e}")
            return None
    
    def _update_stats(self, cursor, user_id, emotion):
        """Helper to update the counts"""
        cursor.execute('''
            SELECT id, count FROM emotion_stats
            WHERE user_id = ? AND emotion = ?
        ''', (user_id, emotion))
        
        row = cursor.fetchone()
        
        if row:
            cursor.execute('''
                UPDATE emotion_stats
                SET count = count + 1, last_detected = ?
                WHERE id = ?
            ''', (datetime.now(), row[0]))
        else:
            cursor.execute('''
                INSERT INTO emotion_stats (user_id, emotion, count)
                VALUES (?, ?, 1)
            ''', (user_id, emotion))
    
    def get_user_history(self, user_id, limit=10):
        """Fetches recent history"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, detection_time, num_faces, emotions_detected, average_confidence
                FROM detection_history
                WHERE user_id = ?
                ORDER BY detection_time DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                history.append({
                    'id': row[0],
                    'time': row[1],
                    'num_faces': row[2],
                    'emotions': json.loads(row[3]),
                    'confidence': row[4]
                })
            
            return history
            
        except Exception as e:
            print(f"History lookup failed: {e}")
            return []
    
    def get_emotion_statistics(self, user_id):
        """Gets the aggregate stats"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT emotion, count, last_detected
                FROM emotion_stats
                WHERE user_id = ?
                ORDER BY count DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            stats = {}
            for row in rows:
                stats[row[0]] = {
                    'count': row[1],
                    'last_detected': row[2]
                }
            
            return stats
            
        except Exception as e:
            print(f"Stats lookup failed: {e}")
            return {}
    
    def get_total_detections(self, user_id):
        """Counts total detections"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM detection_history
                WHERE user_id = ?
            ''', (user_id,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception as e:
            print(f"Count lookup failed: {e}")
            return 0
