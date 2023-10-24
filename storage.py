from mysql.connector import MySQLConnection
import time

# Hàm để kết nối đến cơ sở dữ liệu MySQL
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",  
            password="minhQuanLOV3",  # Thay thế bằng mật khẩu MySQL của bạn
            database="cbs_para"  # Thay thế bằng tên cơ sở dữ liệu MySQL của bạn
        )
        return conn
    except Exception as e:
        print(f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

# Hàm để tạo và cập nhật giá trị x, g, p
def update_values(conn):
    cursor = conn.cursor()
    while True:
        # Thực hiện hàm cố định để tính toán giá trị x, g, p
        x, g, p = calculate_values()
        
        # Lưu trữ giá trị vào cơ sở dữ liệu
        insert_query = "INSERT INTO values (x, g, p) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (x, g, p))
        conn.commit()
        
        print(f"Updated values: x={x}, g={g}, p={p}")
        
        # Chờ 5 phút trước khi tạo giá trị mới
        time.sleep(300)  # 300 giây = 5 phút

# Hàm cố định để tính toán giá trị x, g, p (giả sử)
def calculate_values():
    # Đây là nơi bạn có thể triển khai hàm cố định để tính toán giá trị x, g, p
    # Ví dụ: x, g, p = tinh_toan_x_g_p()
    # Trong ví dụ này, chúng tôi sử dụng các giá trị tĩnh để minh họa
    x = 42.0
    g = 9.8
    p = 3.14
    return x, g, p

if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        update_values(conn)
