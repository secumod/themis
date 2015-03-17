import psycopg2;
import scell;

password="password";

def init_table(conn):
    cur = conn.cursor();
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('scell_data',));
    if cur.fetchone()[0]==False:
        cur.execute("CREATE TABLE scell_data (id serial PRIMARY KEY, num bytea, data bytea);");
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('scell_data_auth',));
    if cur.fetchone()[0]==False:
        cur.execute("CREATE TABLE scell_data_auth (id serial PRIMARY KEY, num bytea, data bytea);");
    conn.commit();
    cur.close();

def add_record(conn, field1, field2):
    enc=scell.scell_auto_split(password);
    enc_field1, field1_auth_data = enc.encrypt(str(field1));
    enc_field2, field2_auth_data = enc.encrypt(str(field2));
    
    cur = conn.cursor();
    cur.execute("INSERT INTO scell_data (num, data) VALUES (%s, %s) RETURNING ID",(psycopg2.Binary(enc_field1), psycopg2.Binary(enc_field2)));
    new_id_value=cur.fetchone()[0];
    cur.execute("INSERT INTO scell_data_auth (id, num, data) VALUES (%s, %s, %s)",(new_id_value, psycopg2.Binary(field1_auth_data), psycopg2.Binary(field2_auth_data)));
    conn.commit();
    cur.close();
    return new_id_value;

def get_record(conn, id):
    dec=scell.scell_auto_split(password);
    cur = conn.cursor();
    cur.execute("SELECT * FROM scell_data INNER JOIN scell_data_auth ON scell_data.id = %s AND scell_data.id=scell_data_auth.id;", (id,))
    x = cur.fetchone();
    print "stored data:", repr(str(x[1])), repr(str(x[4])), repr(str(x[2])), repr(str(x[5]));
    num=dec.decrypt(str(x[1]),str(x[4]));
    data=dec.decrypt(str(x[2]),str(x[5]));
    cur.close();
    return (num,data);


conn = psycopg2.connect("dbname=scell_auto_split_test user=postgres");
init_table(conn);
id=add_record(conn, "First record", "Second record");
rec=get_record(conn, id);
print "real_data: ", rec;
conn.close();



