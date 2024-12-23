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


