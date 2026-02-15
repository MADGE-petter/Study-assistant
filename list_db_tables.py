import datetime
import sqlite3

DATABASE_NAME = (
    "C:\\Users\\ADMIN\\OneDrive\\Máy tính\\STUDY ASSISTANT\\study_assistant.db"
)


def get_table_schema_and_pk(cursor, table_name):
    """
    Truy xuất tên cột, kiểu dữ liệu và thông tin khóa chính cho một bảng đã cho.
    Trả về một danh sách các tuple (tên_cột, kiểu_dữ_liệu, là_khóa_chính)
    và một danh sách các tên cột là khóa chính.
    """
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor.fetchall()
    schema_details = []
    pk_columns = []
    for col in columns_info:
        col_name = col[1]  # Tên cột
        col_type = col[2]  # Kiểu dữ liệu
        is_pk = bool(col[5])  # col[5] là cờ PK
        schema_details.append((col_name, col_type, is_pk))
        if is_pk:
            pk_columns.append(col_name)
    return schema_details, pk_columns


def get_foreign_key_info(cursor, table_name):
    """
    Truy xuất chi tiết khóa ngoại cho một bảng đã cho.
    Trả về một danh sách các dict chứa thông tin FK.
    """
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    fk_info = cursor.fetchall()
    foreign_keys = []
    for fk in fk_info:
        # Cấu trúc của mỗi hàng fk:
        # (id, seq, table, from, to, on_update, on_delete, match)
        # fk[2]: tên bảng được tham chiếu (parent table)
        # fk[3]: tên cột trong bảng hiện tại (child column)
        # fk[4]: tên cột trong bảng được tham chiếu (parent column)
        foreign_keys.append(
            {
                "from_column": fk[3],
                "to_table": fk[2],
                "to_column": fk[4],
            }
        )
    return foreign_keys


def get_table_data(cursor, table_name):
    """Truy xuất tất cả dữ liệu từ một bảng đã cho."""
    cursor.execute(f"SELECT * FROM {table_name};")
    return cursor.fetchall()


def display_table_report(table_name):
    """
    Kết nối với cơ sở dữ liệu, tìm nạp lược đồ, khóa chính, khóa ngoại và dữ liệu,
    sau đó in ra ở định dạng dễ đọc để làm báo cáo.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        print(f"Báo cáo cho bảng: {table_name.upper()}")
        print("=" * (20 + len(table_name)))

        # Lấy lược đồ và thông tin khóa chính
        schema_details, pk_columns = get_table_schema_and_pk(cursor, table_name)
        if not schema_details:
            print(f"Không tìm thấy lược đồ cho bảng '{table_name}'.")
            return

        print("\nCấu trúc bảng (Schema):")
        for i, (col_name, col_type, is_pk) in enumerate(schema_details):
            pk_indicator = " (PK)" if is_pk else ""
            print(f"  {i + 1}. {col_name} ({col_type}){pk_indicator}")

        # Lấy thông tin khóa ngoại
        foreign_keys = get_foreign_key_info(cursor, table_name)
        if foreign_keys:
            print("\nKhóa ngoại (Foreign Keys):")
            for fk in foreign_keys:
                print(
                    f"  - Cột '{fk['from_column']}' tham chiếu đến '{fk['to_table']}.{fk['to_column']}'"
                )
        else:
            print("\nKhông có khóa ngoại nào.")

        # Lấy và hiển thị dữ liệu
        data = get_table_data(cursor, table_name)
        if not data:
            print(f"\nKhông có dữ liệu trong bảng '{table_name}'.")
            print("\n")  # Thêm một dòng trống để nhất quán trước bảng tiếp theo
            return

        print(f"\nDữ liệu trong bảng '{table_name}':")

        # Xác định chiều rộng cột để định dạng cơ bản
        column_names = [col[0] for col in schema_details]
        col_widths = [len(col) for col in column_names]
        for row in data:
            for i, item in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(item)))

        # In tiêu đề
        header_line = " | ".join(
            col.ljust(width) for col, width in zip(column_names, col_widths)
        )
        print(header_line)
        print("-" * len(header_line))

        # In các hàng dữ liệu
        for row in data:
            row_line = " | ".join(
                str(item).ljust(width) for item, width in zip(row, col_widths)
            )
            print(row_line)

        print("\n")

    except sqlite3.Error as e:
        print(f"Lỗi cơ sở dữ liệu khi xử lý bảng '{table_name}': {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    tables_to_report = [
        "notes",
        "tasks",
        "reminders",
    ]  # Giả sử đây là các bảng chính cần báo cáo
    for table in tables_to_report:
        display_table_report(table)
