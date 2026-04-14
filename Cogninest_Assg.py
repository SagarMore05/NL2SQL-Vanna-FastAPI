import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# -----------------------------
# STEP 1: CREATE TABLES
# -----------------------------

cursor.executescript("""

DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS invoices;

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    department TEXT,
    phone TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
);

""")

# -----------------------------
# STEP 2: INSERT DOCTORS
# -----------------------------

specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

doctors = []
for _ in range(15):
    name = fake.name()
    spec = random.choice(specializations)
    dept = spec + " Dept"
    phone = fake.phone_number()
    
    cursor.execute(
        "INSERT INTO doctors (name, specialization, department, phone) VALUES (?, ?, ?, ?)",
        (name, spec, dept, phone)
    )
    doctors.append(cursor.lastrowid)

# -----------------------------
# STEP 3: INSERT PATIENTS
# -----------------------------

cities = ["Mumbai", "Pune", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Ahmedabad", "Nagpur"]

patients = []
for _ in range(200):
    first = fake.first_name()
    last = fake.last_name()
    email = fake.email() if random.random() > 0.2 else None  # NULL sometimes
    phone = fake.phone_number() if random.random() > 0.2 else None
    dob = fake.date_of_birth(minimum_age=1, maximum_age=90)
    gender = random.choice(["M", "F"])
    city = random.choice(cities)
    reg_date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    cursor.execute(
        "INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (first, last, email, phone, dob, gender, city, reg_date)
    )
    patients.append(cursor.lastrowid)

# -----------------------------
# STEP 4: INSERT APPOINTMENTS
# -----------------------------

statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]
appointments = []

for _ in range(500):
    patient_id = random.choice(patients)
    doctor_id = random.choice(doctors)
    date = datetime.now() - timedelta(days=random.randint(0, 365))
    status = random.choice(statuses)
    notes = fake.sentence() if random.random() > 0.3 else None
    
    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES (?, ?, ?, ?, ?)",
        (patient_id, doctor_id, date, status, notes)
    )
    appointments.append((cursor.lastrowid, status))

# -----------------------------
# STEP 5: INSERT TREATMENTS
# -----------------------------

treatment_names = ["X-Ray", "MRI", "Blood Test", "Surgery", "Consultation"]

for appt_id, status in random.sample(appointments, 350):
    if status == "Completed":
        name = random.choice(treatment_names)
        cost = round(random.uniform(50, 5000), 2)
        duration = random.randint(10, 120)
        
        cursor.execute(
            "INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes) VALUES (?, ?, ?, ?)",
            (appt_id, name, cost, duration)
        )

# -----------------------------
# STEP 6: INSERT INVOICES
# -----------------------------

invoice_status = ["Paid", "Pending", "Overdue"]

for _ in range(300):
    patient_id = random.choice(patients)
    total = round(random.uniform(100, 10000), 2)
    paid = total if random.random() > 0.3 else round(total * random.uniform(0, 0.8), 2)
    status = random.choice(invoice_status)
    date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    cursor.execute(
        "INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status) VALUES (?, ?, ?, ?, ?)",
        (patient_id, date, total, paid, status)
    )

# -----------------------------
# FINALIZE
# -----------------------------

conn.commit()
conn.close()

print("Database created successfully!")