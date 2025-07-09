import mysql.connector 

# --- Database Connection ---
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="judie",  # Change if needed
        database="ong",
        port=3307  # Default MySQL port
    )

# --- PN CRUD ---
def list_pn():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pn")
    rows = cursor.fetchall()
    print("\n--- PN List ---")
    for row in rows:
        print(f"ID: {row[0]}, Sigle: {row[1]}, Country: {row[2]}")
    conn.close()

def add_pn():
    sigle = input("Enter PN sigle: ")
    country = input("Enter country: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pn (Sigle, Country) VALUES (%s, %s)", (sigle, country))
    conn.commit()
    print("✅ PN added.")
    conn.close()

def update_pn():
    idpn = input("Enter PN ID to update: ")
    sigle = input("New sigle: ")
    country = input("New country: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE pn SET Sigle=%s, Country=%s WHERE idpn=%s", (sigle, country, idpn))
    conn.commit()
    print("✅ PN updated.")
    conn.close()

def delete_pn():
    idpn = input("Enter PN ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pn WHERE idpn=%s", (idpn,))
    conn.commit()
    print("✅ PN deleted.")
    conn.close()

# --- Kilasy CRUD ---
def list_kilasy():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kilasy.idkilasy, kilasy.sigle, kilasy.location, pn.Sigle 
        FROM kilasy JOIN pn ON kilasy.idpn = pn.idpn
    """)
    rows = cursor.fetchall()
    print("\n--- Kilasy List ---")
    for row in rows:
        print(f"ID: {row[0]}, Sigle: {row[1]}, Location: {row[2]}, PN: {row[3]}")
    conn.close()

def add_kilasy():
    sigle = input("Class sigle: ")
    location = input("Location: ")
    idpn = input("PN ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kilasy (sigle, location, idpn) VALUES (%s, %s, %s)", (sigle, location, idpn))
    conn.commit()
    print("✅ Class added.")
    conn.close()

def update_kilasy():
    idkilasy = input("Enter Kilasy ID to update: ")
    sigle = input("New sigle: ")
    location = input("New location: ")
    idpn = input("New PN ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE kilasy SET sigle=%s, location=%s, idpn=%s WHERE idkilasy=%s", (sigle, location, idpn, idkilasy))
    conn.commit()
    print("✅ Kilasy updated.")
    conn.close()

def delete_kilasy():
    idkilasy = input("Enter Kilasy ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kilasy WHERE idkilasy=%s", (idkilasy,))
    conn.commit()
    print("✅ Kilasy deleted.")
    conn.close()

# --- Student CRUD ---
def list_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT std.idstd, std.firstname, std.lastname, kilasy.sigle 
        FROM std LEFT JOIN kilasy ON std.idkilasy = kilasy.idkilasy
    """)
    rows = cursor.fetchall()
    print("\n--- Students ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Class: {row[3]}")
    conn.close()

def add_student():
    fname = input("First name: ")
    lname = input("Last name: ")
    idkilasy = input("Class ID (idkilasy): ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO std (firstname, lastname, idkilasy) VALUES (%s, %s, %s)", (fname, lname, idkilasy))
    conn.commit()
    print("✅ Student added.")
    conn.close()

def update_student():
    idstd = input("Student ID to update: ")
    fname = input("New first name: ")
    lname = input("New last name: ")
    idkilasy = input("New class ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE std SET firstname=%s, lastname=%s, idkilasy=%s WHERE idstd=%s", (fname, lname, idkilasy, idstd))
    conn.commit()
    print("✅ Student updated.")
    conn.close()

def delete_student():
    idstd = input("Enter student ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM std WHERE idstd=%s", (idstd,))
    conn.commit()
    print("✅ Student deleted.")
    conn.close()

# --- Reports ---
def report_students_by_class():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kilasy.sigle, COUNT(std.idstd)
        FROM kilasy LEFT JOIN std ON kilasy.idkilasy = std.idkilasy
        GROUP BY kilasy.sigle
    """)
    rows = cursor.fetchall()
    print("\n--- Students per Class ---")
    for row in rows:
        print(f"Class: {row[0]}, Students: {row[1]}")
    conn.close()

def report_classes_by_pn():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pn.Sigle, COUNT(kilasy.idkilasy)
        FROM pn LEFT JOIN kilasy ON pn.idpn = kilasy.idpn
        GROUP BY pn.Sigle
    """)
    rows = cursor.fetchall()
    print("\n--- Classes per PN ---")
    for row in rows:
        print(f"PN: {row[0]}, Classes: {row[1]}")
    conn.close()

def report_full_details():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT std.firstname, std.lastname, kilasy.sigle, kilasy.location, pn.Sigle
        FROM std
        JOIN kilasy ON std.idkilasy = kilasy.idkilasy
        JOIN pn ON kilasy.idpn = pn.idpn
    """)
    rows = cursor.fetchall()
    print("\n--- Full Report ---")
    for row in rows:
        print(f"Student: {row[0]} {row[1]}, Class: {row[2]}, Location: {row[3]}, PN: {row[4]}")
    conn.close()

# --- Menus ---
def pn_menu():
    while True:
        print("\n-- PN Management --")
        print("1. List")
        print("2. Add")
        print("3. Update")
        print("4. Delete")
        print("5. Back")
        choice = input("Choice: ")
        if choice == '1': list_pn()
        elif choice == '2': add_pn()
        elif choice == '3': update_pn()
        elif choice == '4': delete_pn()
        elif choice == '5': break
        else: print("❌ Invalid choice")

def kilasy_menu():
    while True:
        print("\n-- Kilasy Management --")
        print("1. List")
        print("2. Add")
        print("3. Update")
        print("4. Delete")
        print("5. Back")
        choice = input("Choice: ")
        if choice == '1': list_kilasy()
        elif choice == '2': add_kilasy()
        elif choice == '3': update_kilasy()
        elif choice == '4': delete_kilasy()
        elif choice == '5': break
        else: print("❌ Invalid choice")

def std_menu():
    while True:
        print("\n-- Student Management --")
        print("1. List")
        print("2. Add")
        print("3. Update")
        print("4. Delete")
        print("5. Back")
        choice = input("Choice: ")
        if choice == '1': list_students()
        elif choice == '2': add_student()
        elif choice == '3': update_student()
        elif choice == '4': delete_student()
        elif choice == '5': break
        else: print("❌ Invalid choice")

def report_menu():
    while True:
        print("\n-- Reports --")
        print("1. Students per class")
        print("2. Classes per PN")
        print("3. Full student-class-PN listing")
        print("4. Back")
        choice = input("Choice: ")
        if choice == '1': report_students_by_class()
        elif choice == '2': report_classes_by_pn()
        elif choice == '3': report_full_details()
        elif choice == '4': break
        else: print("❌ Invalid choice")

# --- Main Menu ---
def main():
    while True:
        print("\n======= ONG CLI CRUD =======")
        print("1. Manage PN")
        print("2. Manage Kilasy (Classes)")
        print("3. Manage Students")
        print("4. Reports")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1': pn_menu()
        elif choice == '2': kilasy_menu()
        elif choice == '3': std_menu()
        elif choice == '4': report_menu()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == '__main__':
    main()
