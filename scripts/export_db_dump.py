import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from django.db import connection

def export_database_dump():
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    dump_lines = [
        "-- --------------------------------------------------------",
        "-- SafeRide: Complete MySQL Database Dump",
        "-- Compatible with MySQL 8.x, MariaDB & phpMyAdmin",
        "-- --------------------------------------------------------",
        "",
        "SET FOREIGN_KEY_CHECKS=0;",
        "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';",
        "SET time_zone = '+00:00';",
        ""
    ]

    for table in tables:
        dump_lines.append(f"-- Table structure for `{table}`")
        dump_lines.append(f"DROP TABLE IF EXISTS `{table}`;")
        cursor.execute(f"SHOW CREATE TABLE `{table}`")
        create_stmt = cursor.fetchone()[1]
        dump_lines.append(f"{create_stmt};")
        dump_lines.append("")

        cursor.execute(f"SELECT * FROM `{table}`")
        rows = cursor.fetchall()
        if rows:
            dump_lines.append(f"-- Dumping data for table `{table}`")
            col_names = [desc[0] for desc in cursor.description]
            col_str = ", ".join([f"`{c}`" for c in col_names])

            val_rows = []
            for r in rows:
                formatted_vals = []
                for v in r:
                    if v is None:
                        formatted_vals.append("NULL")
                    elif isinstance(v, (int, float)):
                        formatted_vals.append(str(v))
                    elif isinstance(v, bytes):
                        formatted_vals.append("0x" + v.hex())
                    else:
                        escaped = str(v).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")
                        formatted_vals.append(f"'{escaped}'")
                val_rows.append("  (" + ", ".join(formatted_vals) + ")")

            insert_stmt = f"INSERT INTO `{table}` ({col_str}) VALUES\n" + ",\n".join(val_rows) + ";"
            dump_lines.append(insert_stmt)
            dump_lines.append("")

    dump_lines.append("SET FOREIGN_KEY_CHECKS=1;")
    
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saferide_database_dump.sql')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(dump_lines) + "\n")

    print(f"Dump completed: {len(tables)} tables exported to {out_path}")

if __name__ == '__main__':
    export_database_dump()
