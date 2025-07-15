from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import psycopg2
import datetime

app = FastAPI()

def get_db():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="sar@123"
    )

class Software(BaseModel):
    name: str
    version: str
    installed_on: str

class SystemInfo(BaseModel):
    hostname: str
    os: str
    cpu: str
    ram: str
    ip_address: str
    software: List[Software]

@app.post("/register_system/")
def register_system(system: SystemInfo):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO systems (hostname, os, cpu, ram, ip_address, last_seen)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
    """, (system.hostname, system.os, system.cpu, system.ram, system.ip_address, datetime.datetime.now()))
    system_id = cur.fetchone()[0]

    for sw in system.software:
        cur.execute("""
            INSERT INTO software (system_id, name, version, installed_on)
            VALUES (%s, %s, %s, %s);
        """, (system_id, sw.name, sw.version, sw.installed_on))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "System Registered"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import psycopg2
import datetime

app = FastAPI()

# ✅ Allow React frontend (http://localhost:3000) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB connection function
def get_db():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",     # 👈 Change to your DB name if different
        user="postgres",
        password="sar@123"
    )

# ✅ Data Models
class Software(BaseModel):
    name: str
    version: str
    installed_on: str

class SystemInfo(BaseModel):
    hostname: str
    os: str
    cpu: str
    ram: str
    ip_address: str
    software: List[Software]

# ✅ API to Register New System
@app.post("/register_system/")
def register_system(system: SystemInfo):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO systems (hostname, os, cpu, ram, ip_address, last_seen)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """, (
            system.hostname,
            system.os,
            system.cpu,
            system.ram,
            system.ip_address,
            datetime.datetime.now()
        ))
        system_id = cur.fetchone()[0]

        for sw in system.software:
            cur.execute("""
                INSERT INTO software (system_id, name, version, installed_on)
                VALUES (%s, %s, %s, %s);
            """, (system_id, sw.name, sw.version, sw.installed_on))

        conn.commit()
        return {"status": "System Registered"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cur.close()
        conn.close()

# ✅ API to Get All Systems (for React Dashboard)
@app.get("/systems")
def get_systems():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, hostname, os, cpu, ram, ip_address, last_seen
            FROM systems ORDER BY id DESC;
        """)
        rows = cur.fetchall()

        systems = [
            {
                "id": row[0],
                "hostname": row[1],
                "os": row[2],
                "cpu": row[3],
                "ram": row[4],
                "ip_address": row[5],
                "last_seen": row[6]
            }
            for row in rows
        ]

        return systems

    except Exception as e:
        return {"error": str(e)}

    finally:
        cur.close()
        conn.close()
        
@app.get("/software/{system_id}")
def get_software(system_id: int):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT name, version, installed_on
            FROM software
            WHERE system_id = %s
        """, (system_id,))
        rows = cur.fetchall()

        software_list = [
            {
                "name": row[0],
                "version": row[1],
                "installed_on": row[2]
            }
            for row in rows
        ]
        return software_list

    except Exception as e:
        return {"error": str(e)}

    finally:
        cur.close()
        conn.close()
