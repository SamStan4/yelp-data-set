import psycopg2
from private.data_base_details import data_base_info

def sql_clean_string(s : str) -> str:
    new_string = s.replace("'", "''").replace("\n", " ").replace("\t", "").replace("\t", "")
    return new_string

def execute_query(query_string : str):
    try:
        conn = psycopg2.connect(
            dbname=data_base_info.data_base_name,
            user=data_base_info.data_base_user,
            host=data_base_info.data_base_host,
            password=data_base_info.data_base_password
        )
        cur = conn.cursor()
        cur.execute(query_string)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"ERROR -- execute_query() -- {e}")
        return None

def execute_insert(insert_string : str) -> None:
    try:
        conn = psycopg2.connect(
            dbname=data_base_info.data_base_name,
            user=data_base_info.data_base_user,
            host=data_base_info.data_base_host,
            password=data_base_info.data_base_password
        )
        cur = conn.cursor()
        cur.execute(insert_string)
        conn.commit()
    except:
        print("ERROR -- execute_query() --")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()