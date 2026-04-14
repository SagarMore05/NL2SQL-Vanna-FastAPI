from vanna_setup import agent

print("🚀 Preparing memory seed data...")

training_data = [
    # -----------------------------
    # Patient Queries
    # -----------------------------
    ("How many patients do we have?",
     "SELECT COUNT(*) FROM patients"),

    ("Patients from Mumbai",
     "SELECT * FROM patients WHERE city='Mumbai'"),

    ("Which city has most patients?",
     "SELECT city, COUNT(*) FROM patients GROUP BY city ORDER BY COUNT(*) DESC LIMIT 1"),

    # -----------------------------
    # Doctor Queries
    # -----------------------------
    ("List all doctors and their specializations",
     "SELECT name, specialization FROM doctors"),

    ("Doctors in Cardiology",
     "SELECT * FROM doctors WHERE specialization='Cardiology'"),

    ("Appointments per doctor",
     """SELECT d.name, COUNT(*) 
        FROM doctors d
        JOIN appointments a ON d.id = a.doctor_id
        GROUP BY d.name"""),

    # -----------------------------
    # Appointment Queries
    # -----------------------------
    ("Monthly appointments",
     """SELECT strftime('%Y-%m', appointment_date), COUNT(*)
        FROM appointments GROUP BY 1"""),

    ("Appointments in last 30 days",
     """SELECT * FROM appointments
        WHERE appointment_date >= date('now','-30 days')"""),

    ("Cancelled appointments count",
     "SELECT COUNT(*) FROM appointments WHERE status='Cancelled'"),

    # -----------------------------
    # Financial Queries
    # -----------------------------
    ("Show total revenue",
     "SELECT SUM(total_amount) FROM invoices"),

    ("Revenue by month",
     """SELECT strftime('%Y-%m', invoice_date), SUM(total_amount)
        FROM invoices GROUP BY 1"""),

    ("Show unpaid invoices",
     "SELECT * FROM invoices WHERE status != 'Paid'"),

    ("Overdue invoices",
     "SELECT * FROM invoices WHERE status='Overdue'"),

    ("Top 5 patients by spending",
     """SELECT p.first_name, p.last_name, SUM(i.total_amount)
        FROM patients p
        JOIN invoices i ON p.id = i.patient_id
        GROUP BY p.id
        ORDER BY SUM(i.total_amount) DESC LIMIT 5"""),

    # -----------------------------
    # Advanced Query
    # -----------------------------
    ("Patients with more than 3 visits",
     """SELECT patient_id, COUNT(*) 
        FROM appointments 
        GROUP BY patient_id 
        HAVING COUNT(*) > 3"""),

    ("Average treatment cost",
     "SELECT AVG(cost) FROM treatments")
]

# -----------------------------
# Print Q&A pairs (for documentation)
# -----------------------------

for q, sql in training_data:
    print(f"\nQ: {q}")
    print(f"SQL: {sql}")

print("\n Memory seed data prepared (used for documentation & training reference)")