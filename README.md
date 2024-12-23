# zema-astetika
import mysql.connector

connection = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password ="",
    database ="",
)

cursor = connection.cursor()
if connection :
    print("Berhasil Terhubung ke DataBase")

cursor.execute("CREATE DATABASE zema_estetika")
print('DataBase berhasil dibuat')

cursor.execute("show databases")
print(cursor.fetchall())

result = cursor.fetchall()
for item in result :
    print(item)
import mysql.connector

# Koneksi ke database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="zema_estetika"
)

cursor = connection.cursor()

# Membuat tabel pelanggan/customers
query = """CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(15),
        address TEXT,
        tgl_lahir DATE, 
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    )"""
cursor.execute(query)

# Membuat tabel treatment/layanan
query = """CREATE TABLE IF NOT EXISTS layanan (
        service_id INT AUTO_INCREMENT PRIMARY KEY,
        service_name VARCHAR(100),
        description TEXT,
        harga DECIMAL(10,2),
        durasi INT
    )"""
cursor.execute(query)

# Membuat tabel pembayaran/booking
query = """CREATE TABLE IF NOT EXISTS pembayaran (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        service_id INT,
        appointment_date DATE,
        appointment_time TIME,
        status VARCHAR(20),
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (service_id) REFERENCES layanan(service_id)  -- Perbaikan: Mengganti 'services' menjadi 'layanan'
    )"""
cursor.execute(query)

# Membuat tabel staff/karyawan
query = """CREATE TABLE IF NOT EXISTS staff (
        staff_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        position VARCHAR(50),
        phone VARCHAR(15)
    )"""  
cursor.execute(query)

# Membuat tabel transaksi
query = """CREATE TABLE IF NOT EXISTS transaksi (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        appointment_id INT,
        customer_id INT,
        service_id INT,
        staff_id INT,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount DECIMAL(10,2),
        metode_pembayaran VARCHAR(50),
        FOREIGN KEY (appointment_id) REFERENCES pembayaran(appointment_id),  # Perbaikan: Mengganti 'appointments' menjadi 'pembayaran'
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (service_id) REFERENCES layanan(service_id),  # Perbaikan: Mengganti 'services' menjadi 'layanan'
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )"""
cursor.execute(query)

# Membuat tabel produk yang dijual
query = """CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(100),
        description TEXT,
        price DECIMAL(10,2),
        stock INT,
        category VARCHAR(50)
    )"""
cursor.execute(query)



# Menampilkan semua tabel dalam database zema_estetika
print("\nMenampilkan semua tabel dalam database zema_estetika:")
cursor.execute("SHOW TABLES")
for table in cursor:
    print(table)


connection.close()
import mysql.connector
from colorama import Fore, Style, init
from prettytable import PrettyTable


init(autoreset=True)  # Inisialisasi Colorama untuk reset otomatis warna

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="zema_estetika"
)

def welcome_message():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + Style.BRIGHT + "\tSistem zema estetika")
    print(Fore.CYAN + "=" * 50)

def insert_customer(connection):
    print(Fore.CYAN + "\n--- Tambah Data Pelanggan ---")
    name = input("Masukkan nama: ")
    phone = input("Masukkan nomor telepon: ")
    address = input("Masukkan alamat: ")
    tgl_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")

    cursor = connection.cursor()
    query = "INSERT INTO customers (name, phone, address, tgl_lahir) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, phone, address, tgl_lahir))
    connection.commit()
    print(Fore.GREEN + f"{cursor.rowcount} data berhasil disimpan")

def insert_many_customers(connection):
    print(Fore.CYAN + "\n--- Tambah Banyak Data Pelanggan ---")
    cursor = connection.cursor()
    customers_data = []

    while True:
        name = input("Masukkan nama (atau 'selesai' untuk berhenti): ")
        if name.lower() == 'selesai':
            break
        
        phone = input("Masukkan nomor telepon: ")
        address = input("Masukkan alamat: ")
        tgl_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
        
        customers_data.append((name, phone, address, tgl_lahir))

    if customers_data:
        query = "INSERT INTO customers (name, phone, address, tgl_lahir) VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, customers_data)
        connection.commit()
        print(Fore.GREEN + f"{cursor.rowcount} data berhasil disimpan")
    else:
        print(Fore.YELLOW + "Tidak ada data yang dimasukkan.")

def show_customers(connection):
    print(Fore.CYAN + "\n--- Daftar Pelanggan ---")
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM customers"
        cursor.execute(sql)
        result = cursor.fetchall()

        if not result:
            print(Fore.YELLOW + "Tidak ada data customer.")
            return

        table = PrettyTable()
        table.field_names = ["ID", "Nama", "No. Telepon", "Alamat", "Tgl Lahir"]
        for customer in result:
            tgl_lahir = customer[4] if customer[4] else "-"
            table.add_row([customer[0], customer[1], customer[2], customer[3], tgl_lahir])
        print(table)
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")

def update_customer(connection):
    print(Fore.CYAN + "\n--- Update Data Pelanggan ---")
    try:
        show_customers(connection)

        customer_id = input(Fore.YELLOW + "\nPilih ID customer yang akan diupdate (0 untuk batal): ")
        if customer_id == "0":
            print(Fore.YELLOW + "Update dibatalkan.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        existing_customer = cursor.fetchone()

        if not existing_customer:
            print(Fore.RED + "Error: ID customer tidak ditemukan.")
            return

        print(Fore.GREEN + "\nBiarkan kosong jika tidak ingin mengubah data")
        print(Fore.BLUE + f"Nama saat ini: {existing_customer[1]}")
        print(Fore.BLUE + f"No. Telepon saat ini: {existing_customer[2]}")
        print(Fore.BLUE + f"Alamat saat ini: {existing_customer[3]}")
        print(Fore.BLUE + f"Tanggal Lahir saat ini: {existing_customer[4]}")

        name = input("Nama baru: ") or existing_customer[1]
        phone = input("No. Telepon baru: ") or existing_customer[2]
        address = input("Alamat baru: ") or existing_customer[3]
        tgl_lahir = input("Tanggal Lahir baru (YYYY-MM-DD): ") or existing_customer[4]

        query = "UPDATE customers SET name = %s, phone = %s, address = %s, tgl_lahir = %s WHERE customer_id = %s"
        cursor.execute(query, (name, phone, address, tgl_lahir, customer_id))
        connection.commit()
        print(Fore.GREEN + "\nData berhasil diupdate!")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")

def delete_customer(connection):
    print(Fore.CYAN + "\n--- Hapus Data Pelanggan ---")
    try:
        show_customers(connection)

        customer_id = input(Fore.YELLOW + "\nPilih ID customer yang akan dihapus (0 untuk batal): ")
        if customer_id == "0":
            print(Fore.YELLOW + "Penghapusan dibatalkan.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT name FROM customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()

        if not customer:
            print(Fore.RED + "Error: ID customer tidak ditemukan.")
            return

        confirm = input(Fore.RED + f"\nAnda yakin ingin menghapus customer {customer[0]}? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "Penghapusan dibatalkan.")
            return

        query = "DELETE FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        connection.commit()
        print(Fore.GREEN + "\nData berhasil dihapus!")
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")

def search_customer(connection):
    print(Fore.CYAN + "\n--- Cari Data Pelanggan ---")
    try:
        keyword = input(Fore.YELLOW + "Masukkan kata kunci (nama/alamat): ").strip()

        if not keyword:
            print(Fore.RED + "Error: Kata kunci tidak boleh kosong!")
            return

        cursor = connection.cursor()
        sql = "SELECT * FROM customers WHERE name LIKE %s OR address LIKE %s"
        cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
        result = cursor.fetchall()

        if not result:
            print(Fore.YELLOW + "\nTidak ada data yang ditemukan!")
            return

        table = PrettyTable()
        table.field_names = ["ID", "Nama", "No. Telepon", "Alamat", "Tgl Lahir"]
        for customer in result:
            tgl_lahir = customer[4] if customer[4] else "-"
            table.add_row([customer[0], customer[1], customer[2], customer[3], tgl_lahir])

        print(Fore.GREEN + f"\nHasil pencarian untuk '{keyword}':")
        print(table)
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")

welcome_message()
        
#function pada layanan yang tersedia
def insert_layanan(connection):
    """Fungsi untuk memasukkan data layanan secara manual"""
    try:
        cursor = connection.cursor()
        
        # Meminta input dari pengguna
        service_name = input("Masukkan nama layanan: ")
        description = input("Masukkan deskripsi layanan: ")
        
        # Memastikan input harga dan durasi valid
        while True:
            try:
                price = float(input("Masukkan harga layanan: "))
                break
            except ValueError:
                print("Harga harus berupa angka. Silakan coba lagi.")
        
        while True:
            try:
                duration = int(input("Masukkan durasi layanan (dalam menit): "))
                break
            except ValueError:
                print("Durasi harus berupa angka. Silakan coba lagi.")

        query = """INSERT INTO layanan (service_name, description, harga, durasi) 
                   VALUES (%s, %s, %s, %s)"""
        
        cursor.execute(query, (service_name, description, price, duration))
        connection.commit()
        print(f"Layanan '{service_name}' berhasil disimpan. ID layanan yang baru: {cursor.lastrowid}")
    except mysql.connector.Error as error:
        print(f"Error saat memasukkan data layanan: {error}")
    finally:
        cursor.close()

def show_layanan(connection):
    """Fungsi untuk menampilkan semua data layanan"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM layanan")
        results = cursor.fetchall()

        if results:
            print("Daftar Layanan:")
            for service in results:
                print(f"ID: {service[0]}, Nama: {service[1]}, Deskripsi: {service[2]}, Harga: {service[3]}, Durasi: {service[4]} menit")
        else:
            print("Tidak ada data layanan ditemukan.")
    except mysql.connector.Error as error:
        print(f"Error saat menampilkan data layanan: {error}")
    finally:
        cursor.close()

#fungsion pembayaran
def insert_pembayaran(connection):

    cursor = connection.cursor()
    customers = show_customers(connection)
    print("\nDaftar Customers:")
    for customer in customers:
        print(f"ID: {customer[0]}, Nama: {customer[1]}")
        
    customer_id = input("Pilih ID customer: ")
        
    # Tampilkan daftar layanan
    layanan = show_layanan(connection)
    print("\nDaftar Layanan:")
    for service in layanan:
        print(f"ID: {service[0]}, Nama: {service[1]}")
        
    service_id = input("Pilih ID layanan: ")
        
    # Input data booking
    appointment_date = input("Masukkan tanggal booking (YYYY-MM-DD): ")
    appointment_time = input("Masukkan waktu booking (HH:MM:SS): ")
    status = input("Masukkan status booking (Pending/Confirmed/Completed): ")
    notes = input("Catatan tambahan (opsional): ")

    query = """INSERT INTO pembayaran (customer_id, service_id, appointment_date, appointment_time, status, notes) VALUES (%s, %s, %s, %s, %s, %s)"""
        
    cursor.execute(query, (customer_id, service_id, appointment_date, appointment_time, status, notes))
    connection.commit()
    print("{} data booking berhasil disimpan",format(cursor.rowcount))

def show_pembayaran(connection):

    cursor = connection.cursor()
    sql = """SELECT p.appointment_id, c.name, l.service_name, 
                        p.appointment_date, p.appointment_time, 
                        p.status, p.notes
                 FROM pembayaran p
                 JOIN customers c ON p.customer_id = c.customer_id
                 JOIN layanan l ON p.service_id = l.service_id"""
    cursor.execute(sql)
    result = cursor.fetchall()

    if cursor.rowcount <= 0:
        print("Tidak ada data booking")
    else:
        print("Data Booking:")
        for data in result:
            print(f"ID: {data[0]}, Customer: {data[1]}, Layanan: {data[2]}, "
                      f"Tanggal: {data[3]}, Waktu: {data[4]}, "
                      f"Status: {data[5]}, Catatan: {data[6]}")

def update_pembayaran(connection):

    cursor = connection.cursor()
    show_pembayaran(connection)
    appointment_id = input("Pilih ID booking yang akan diupdate: ")
        
    # Tampilkan daftar customers
    customers = show_customers(connection)
    print("\nDaftar Customers:")
    for customer in customers:
        print(f"ID: {customer[0]}, Nama: {customer[1]}")
        
    # Tampilkan daftar layanan
    layanan = show_layanan(connection)
    print("\nDaftar Layanan:")
    for service in layanan:
        print(f"ID: {service[0]}, Nama: {service[1]}")
        
    customer_id = input("Masukkan ID customer baru (kosongkan jika tidak diubah): ")
    service_id = input("Masukkan ID layanan baru (kosongkan jika tidak diubah): ")
    appointment_date = input("Masukkan tanggal booking baru (kosongkan jika tidak diubah): ")
    appointment_time = input("Masukkan waktu booking baru (kosongkan jika tidak diubah): ")
    status = input("Masukkan status booking baru (kosongkan jika tidak diubah): ")
    notes = input("Masukkan catatan baru (kosongkan jika tidak diubah): ")

    sql = "UPDATE customer SET customer_id =%s, service_id =%s, appointment_date =%s, appointment_time =%s, status =%s, notes =%s "
    cursor.execute(sql, (customer_id, service_id, appointment_date, appointment_time, status, notes))
    connection.commit()
    print("{}data berhasil diubah".format(cursor.rowcount))


#funsion untuk staff
def insert_staff(connection):

    cursor = connection.cursor()
    name = input("Masukkan nama staff: ")
    position = input("Masukkan posisi staff: ")
    phone = input("Masukkan nomor telepon staff: ")

    query = "INSERT INTO staff (name, position, phone) VALUES (%s, %s, %s)"
        
    cursor.execute(query, (name, position, phone))
    connection.commit()
    print(f"Data staff '{name}' berhasil disimpan.")

def delete_staff(connection):

    cursor = connection.cursor()
    staff_id = input("Masukkan ID staff yang ingin dihapus: ")
        
    query = "DELETE FROM staff WHERE staff_id = %s"
    cursor.execute(query, (staff_id,))
    connection.commit()
        
    if cursor.rowcount > 0:
        print(f"Data staff dengan ID {staff_id} berhasil dihapus.")
    else:
        print(f"ID staff {staff_id} tidak ditemukan.")
    
def update_staff(connection):

    cursor = connection.cursor()
    staff_id = input("Masukkan ID staff yang ingin diperbarui: ")

        # Menampilkan data staff yang ada
    cursor.execute("SELECT * FROM staff WHERE staff_id = %s", (staff_id,))
    staff = cursor.fetchone()

    if staff:
        print("Data Staff Saat Ini:")
        print(f"ID: {staff[0]}, Nama: {staff[1]}, Posisi: {staff[2]}, Telepon: {staff[3]}")

        # Mengambil input baru
        name = input("Masukkan nama baru (kosongkan jika tidak diubah): ")
        position = input("Masukkan posisi baru (kosongkan jika tidak diubah): ")
        phone = input("Masukkan nomor telepon baru (kosongkan jika tidak diubah): ")

        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        else:
            params.append(staff[1])  # Ambil nama lama

        if position:
            update_fields.append("position = %s")
            params.append(position)
        else:
            params.append(staff[2])  # Ambil posisi lama

        if phone:
            update_fields.append("phone = %s")
            params.append(phone)
        else:
            params.append(staff[3])  # Ambil telepon lama

        params.append(staff_id)

        # Menjalankan query update
        if update_fields:
            sql = f"UPDATE staff SET {', '.join(update_fields)} WHERE staff_id = %s"
            cursor.execute(sql, params)
            connection.commit()
            print(f"Data staff dengan ID {staff_id} berhasil diperbarui.")
        else:
            print("Tidak ada perubahan yang dilakukan.")
    else:
        print("Staff tidak ditemukan.")

def show_staff(connection):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staff")
    results = cursor.fetchall()

    if results:
        print("Daftar Staff:")
        for staff in results:
            print(f"ID: {staff[0]}, Nama: {staff[1]}, Posisi: {staff[2]}, Telepon: {staff[3]}")
    else:
        print("Tidak ada data staff ditemukan.")
    

#funcion untuk transaksi
import mysql.connector

def insert_transaksi(connection):
    """Fungsi untuk memasukkan data transaksi secara manual"""
    try:
        cursor = connection.cursor()
        
        show_customers(connection)
        customer_id = input("Masukkan ID Pelanggan: ")
        show_layanan(connection)
        service_id = input("Masukkan ID Layanan: ")
        show_staff(connection)
        staff_id = input("Masukkan ID Staff: ")
        
        # Memastikan input jumlah transaksi valid
        while True:
            try:
                amount = input("Masukkan Jumlah Transaksi: ")
                break
            except ValueError:
                print("Jumlah transaksi harus berupa angka. Silakan coba lagi.")
        

        query = """INSERT INTO transaksi ( customer_id, service_id, staff_id, amount) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, ( customer_id, service_id, staff_id, amount))
        connection.commit()
        print("Data transaksi berhasil disimpan.")
    except mysql.connector.Error as error:
        print(f"Error saat memasukkan data transaksi: {error}")
    finally:
        cursor.close()

def delete_transaksi(connection):
    """Fungsi untuk menghapus data transaksi berdasarkan ID"""
    try:
        cursor = connection.cursor()
        transaction_id = input("Masukkan ID Transaksi yang ingin dihapus: ")
        
        query = "DELETE FROM transaksi WHERE transaction_id = %s"
        cursor.execute(query, (transaction_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Data transaksi dengan ID {transaction_id} berhasil dihapus.")
        else:
            print(f"ID transaksi {transaction_id} tidak ditemukan.")
    except mysql.connector.Error as error:
        print(f"Error saat menghapus data transaksi: {error}")
    finally:
        cursor.close()

def update_transaksi(connection):
    """Fungsi untuk memperbarui data transaksi berdasarkan ID"""
    try:
        cursor = connection.cursor()
        transaction_id = input("Masukkan ID Transaksi yang ingin diperbarui: ")

        # Menampilkan data transaksi yang ada
        cursor.execute("SELECT * FROM transaksi WHERE transaction_id = %s", (transaction_id,))
        transaksi = cursor.fetchone()

        if transaksi:
            print("Data Transaksi Saat Ini:")
            print(f"ID: {transaksi[0]}, Appointment ID: {transaksi[1]}, Customer ID: {transaksi[2]}, "
                  f"Service ID: {transaksi[3]}, Staff ID: {transaksi[4]}, Amount: {transaksi[5]}, "
                  f"Metode Pembayaran: {transaksi[6]}")

            # Mengambil input baru
            appointment_id = input("Masukkan ID Janji Temu baru (kosongkan jika tidak diubah): ")
            customer_id = input("Masukkan ID Pelanggan baru (kosongkan jika tidak diubah): ")
            service_id = input("Masukkan ID Layanan baru (kosongkan jika tidak diubah): ")
            staff_id = input("Masukkan ID Staff baru (kosongkan jika tidak diubah): ")
            
            # Memastikan input jumlah transaksi valid
            while True:
                amount_input = input("Masukkan Jumlah Transaksi baru (kosongkan jika tidak diubah): ")
                if amount_input == "":
                    amount = transaksi[5]  # Ambil amount lama
                    break
                try:
                    amount = float(amount_input)
                    break
                except ValueError:
                    print("Jumlah transaksi harus berupa angka. Silakan coba lagi.")

            metode_pembayaran_input = input("Masukkan Metode Pembayaran baru (kosongkan jika tidak diubah): ")

            update_fields = []
            params = []

            if appointment_id:
                update_fields.append("appointment_id = %s")
                params.append(appointment_id)
            else:
                params.append(transaksi[1])  # Ambil appointment_id lama

            if customer_id:
                update_fields.append("customer_id = %s")
                params.append(customer_id)
            else:
                params.append(transaksi[2])  # Ambil customer_id lama

            if service_id:
                update_fields.append("service_id = %s")
                params.append(service_id)
            else:
                params.append(transaksi[3])  # Ambil service_id lama

            if staff_id:
                update_fields.append("staff_id = %s")
                params.append(staff_id)
            else:
                params.append(transaksi[4])  # Ambil staff_id lama

            params.append(amount)  # Masukkan amount yang baru
            params.append(metode_pembayaran_input if metode_pembayaran_input else transaksi[6])  # Metode baru atau lama
            params.append(transaction_id)

            # Menjalankan query update
            if update_fields:
                sql = f"UPDATE transaksi SET {', '.join(update_fields)}, amount = %s, metode_pembayaran = %s WHERE transaction_id = %s"
                cursor.execute(sql, params)
                connection.commit()
                print(f"Data transaksi dengan ID {transaction_id} berhasil diperbarui.")
            else:
                print("Tidak ada perubahan yang dilakukan.")
        else:
            print("Transaksi tidak ditemukan.")
    except mysql.connector.Error as error:
        print(f"Error saat memperbarui data transaksi: {error}")
    finally:
        cursor.close()

def show_transaksi(connection):
    """Fungsi untuk menampilkan semua data transaksi"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transaksi")
        results = cursor.fetchall()

        if results:
            print("Daftar Transaksi:")
            for transaksi in results:
                print(f"ID: {transaksi[0]}, Appointment ID: {transaksi[1]}, Customer ID: {transaksi[2]}, "
                      f"Service ID: {transaksi[3]}, Staff ID: {transaksi[4]}, Jumlah: {transaksi[5]}, "
                      f"Metode Pembayaran: {transaksi[6]}")
        else:
            print("Tidak ada data transaksi ditemukan.")
    except mysql.connector.Error as error:
        print(f"Error saat menampilkan data transaksi: {error}")
    finally:
        cursor.close()


#fungsion untuk memasukkan data produck
def insert_products(connection):

        cursor = connection.cursor()
        
        # Data produk yang akan dimasukkan
        products = [
            ("zema moisturizer", "dapat menghidrasi, melindungi, dan meningkatkan elastisitas", 60.00, 40, "pelembab"),
            ("zema sunscreen", "cocok untuk berbagai jenis kulit terutama kulit sensitif", 45.00, 50, "sunscreen"),
            ("zema facial serum", "membantu merawat kulit anda agar terhindar dari penuaan dini", 115.00, 35, "serum"),
            ("zema micellar water", "membantu mengangkat semua kotoran yang menempel dari wajah", 250.00, 10, "pembersih"),
            ("masker wajah", "membantu mengangkat sel kulit mati", 80.00, 40, "masker"),
            ("lip care", "membantu melembabkan bibir", 50.00, 50, "lip")
        ]

        query = """INSERT INTO products (product_name, description, price, stock, category) 
                   VALUES (%s, %s, %s, %s, %s)"""
        
        cursor.executemany(query, products)
        connection.commit()
        print(f"{cursor.rowcount} produk berhasil disimpan.")

def update_stock(connection):
    
    cursor = connection.cursor()
    show_products(connection)
    product_id = input("Masukkan ID Produk yang ingin diubah stoknya: ")
    new_stock = input("Masukkan jumlah stok baru: ")

    query = "UPDATE products SET stock = %s WHERE product_id = %s"
    cursor.execute(query, (new_stock, product_id))
    connection.commit()

    if cursor.rowcount > 0:
        print(f"Stok produk dengan ID {product_id} berhasil diperbarui menjadi {new_stock}.")
    else:
        print(f"ID produk {product_id} tidak ditemukan.")

def show_products(connection):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()

    if results:
        print("Daftar Produk:")
        for product in results:
            print(f"ID: {product[0]}, Nama: {product[1]}, Deskripsi: {product[2]}, Harga: {product[3]}, Stok: {product[4]}, Kategori: {product[5]}")
    else:
        print("Tidak ada data produk ditemukan.")

#laman dalam halaman utama
def show_menu_product(connection):
            
    print("\nPilih Menu:")
    print("1. update product")
    print("2. show product")
    print("3. Exit")

    choice = input("Pilih menu : ")


    if choice == '1':
        update_stock(connection)
    elif choice == '2':
        show_products(connection)
    elif choice == '3':
        show_menu_utama(connection)
    else:
        print("Pilihan tidak valid, silakan coba lagi.")
    
def show_menu_transaksi(connection):
            
    print("\nPilih Menu:")
    print("1. Insert Data Transaksi")
    print("2. Delete Data Transaksi")
    print("3. Update Data Transaksi")
    print("4. Show Data Transaksi")
    print("5. Exit")

    choice = input("Pilih menu (1-5): ")

    if choice == '1':
        insert_transaksi(connection)
    elif choice == '2':
        delete_transaksi(connection)
    elif choice == '3':
        update_transaksi(connection)
    elif choice == '4':
        show_transaksi(connection)
    elif choice == '5':
        show_menu_utama(connection)
    else:
        print("Pilihan tidak valid, silakan coba lagi.")
                

def show_menu_staff(connection):
    
    print("\nPilih Menu:")
    print("1. Insert Data Staff")
    print("2. Delete Data Staff")
    print("3. Update Data Staff")
    print("4. Show Data Staff")
    print("5. Exit")

    choice = input("Pilih menu: ")

    if choice == '1':
        insert_staff(connection)
    elif choice == '2':
        delete_staff(connection)
    elif choice == '3':
        update_staff(connection)
    elif choice == '4':
        show_staff(connection)
    elif choice == '5':
        show_menu_utama
    else:
        print("Pilihan tidak valid, silakan coba lagi.")


def show_menu_customer(connection):
    """Menampilkan menu utama"""
    print("\n===== MANAJEMEN DATA CUSTOMER =====")
    print("1. Insert Satu Customer")
    print("2. Insert Banyak Customer")
    print("3. Tampilkan Semua Customer")
    print("4. Update Customer")
    print("5. Cari Customer")
    print("6. Hapus Customer")
    print("0. Keluar Aplikasi")
    
    menu = input("Pilih Menu > ")

    if menu == "1":
        insert_customer(connection)
    elif menu == "2":
        insert_many_customers(connection)
    elif menu == "3":
        show_customers(connection)
    elif menu == "4":
        update_customer(connection)
    elif menu == "5":
        search_customer(connection)
    elif menu == "6":
        delete_customer(connection)
    elif menu == "0":
        show_menu_utama(connection)
        return False
    else:
        print("Menu tidak valid!")
    return True


def show_menu_pembayaran(connection):
    """Menampilkan menu utama"""
    print("\n===== MANAJEMEN DATA PEMBAYARAN =====")
    print("1. insert pembayaran")
    print("2. show pembayaran")
    print("3. update pembayaran")
    print("0. Keluar Aplikasi")
    
    menu = input("Pilih Menu > ")

    if menu == "1":
        show_customers(connection)
    elif menu == "2":
        insert_pembayaran(connection)
    elif menu == "3":
        up(connection)
    elif menu == "0":
        show_menu_utama(connection)
        return False
    else:
        print("Menu tidak valid!")
    return True

def menu_layanan(connection):
    print("menu")
    print("1. insert layanan")
    print("2. show layanan")

    menu = input("pilih menu: ")

    if menu == "1":
        insert_layanan(connection)
    elif menu == "2":
        show_layanan(connection)
    elif menu == "0":
        show_menu_utama(connection)
    else:
        print("jawaban tidak valid")

#halaman utama yang akan tampil
def show_menu_utama(connection):
    """Menampilkan menu utama"""
    print("\n =====pilihan yang ingin dijalankan=====")
    print("1. menu customer")
    print("2. layanan")
    print("3. menu pembayaran")
    print("4. menu staff")
    print("5. menu transaksi")
    print("6. product")
    print("0. exit")

    menu = input("pilih menu: ")

    if menu == "1":
        show_menu_customer(connection)
    elif menu == "2":
        menu_layanan(connection)
    elif menu == "3":
        show_menu_pembayaran(connection)
    elif menu == "4":
        show_menu_staff(connection)
    elif menu == "5":
        show_menu_transaksi(connection)
    elif menu == "6":
        show_menu_product(connection)
    elif menu == "0":
        print("terimakasih sudah mempercayai kami dalam perawatan anda :)")
        return False
    else:
        print("Menu tidak valid!")
    return True

if __name__ == "__main__":
    while True:
        show_menu_utama(connection)
    
