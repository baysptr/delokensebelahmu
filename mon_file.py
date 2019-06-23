import sys
import time
import datetime
import sqlite3
import hashlib
import requests

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlite3 import Error
from filehash import FileHash

token = '';

class Watcher:
    DIRECTORY_TO_WATCH = "/home/private/Documents/mas_bagus/test"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Penyimpanan:
    def sql_connect():
        try:
            con = sqlite3.connect('logs.db')
            #print("Data Logs Sudah Terhubung")
            return con
        except Error:
            #print("Data Log, belum terhubung. sistem akan berjalan dengan tidak menyimpan LOGS")
            print(Error)

    def crt_tbl(con):
        cObj = con.cursor()
        cObj.execute("create table if not exists m_logs (id integer primary key, mod text not null, desc text not null, enk text not null, tgl text not null)")
        con.commit()
        print("Data Logs Sudah Terhubung")

    def tambah(con, data):
        cObj = con.cursor()
        cObj.execute("insert into m_logs(mod, desc, enk, tgl) values(?,?,?,?)", data)
        #cObj.execute("insert into m_logs (key, enk, tgl) values (?,?,?)", mon, enk, det)
        con.commit()

class Pecah:
    def linear_search(item, my_list):
        found = False
        position = 0
        while position < len(my_list) and not found:
            if my_list[position] == item:
                found = True
            position = position + 1
        return found


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            currentDT = datetime.datetime.now()
            hd = FileHash('md5')
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                print("Created: {}".format(out_text))
                print("Hash: {}".format(hd.hash_file(out_text)))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
                c = Penyimpanan.sql_connect()
                tgl = "{}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second)
                Penyimpanan.tambah(c,("CREATED", out_text, hd.hash_file(out_text), tgl))
                data = {'token': token, 'mode': 'CREATED', 'mon': str(out_text), 'enk': str(hd.hash_file(out_text))}
                req = requests.post('http://192.168.1.11/bagus/push_data.php', data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
                
            #print("Created: {}".format(event.src_path))

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            currentDT = datetime.datetime.now()
            hd = FileHash('md5')
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                print("Modified: {}".format(out_text))
                print("Hash: {}".format(hd.hash_file(out_text)))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
                #print(token)
                c = Penyimpanan.sql_connect()
                tgl = "{}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second)
                mon = '{}'.format(out_text)
                enk = '{}'.format(hd.hash_file(out_text))
                Penyimpanan.tambah(c,("MODIFIED", out_text, hd.hash_file(out_text), tgl))
                data = {'token': token, 'mode': 'MODIFIED', 'mon': str(out_text), 'enk': str(hd.hash_file(out_text))}
                req = requests.post('http://192.168.1.11/bagus/push_data.php', data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
                #print(data)
                #print(req.status_code)
                #print(req.text)
                
            #print("Modified: {}".format(event.src_path))
            #print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            currentDT = datetime.datetime.now()
            hd = hashlib.md5()
            out_text = event.src_path
            itemfound = Pecah.linear_search('swp', out_text.split('.'))
            if itemfound:
                print("...")
            else:
                hd.update(b"Data telah dihapus")
                print("Deleted: {}".format(out_text))
                print("Hash: {}".format(hd.hexdigest()))
                print("Time: {}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second))
                c = Penyimpanan.sql_connect()
                tgl = "{}-{}-{} {}:{}:{}".format(currentDT.day, currentDT.month, currentDT.year, currentDT.hour, currentDT.minute, currentDT.second)
                Penyimpanan.tambah(c,("DELETED", out_text, hd.hexdigest(), tgl))
                data = {'token': token, 'mode': 'DELETED', 'mon': str(out_text), 'enk': str(hd.hexdigest())}
                req = requests.post('http://192.168.1.11/bagus/push_data.php', data, headers={'Content-Type': 'application/x-www-form-urlencoded'})


if __name__ == '__main__':
    val = input("Masukan token anda: ")
    print("Token anda: ")
    print(val)

    data = {'token': str(val)}
    req = requests.post('http://192.168.1.11/bagus/check_token.php', data)

    print(req.status_code)
    #print(req.text)

    if int(req.text) > 0:
        print("Api ditemukan")
        token = str(val)
        w = Watcher()
        c = Penyimpanan.sql_connect()
        Penyimpanan.crt_tbl(c)
        w.run()
    else:
        print("Api tidak ditemukan, Mohon periksa kembali")
        sys.exit()
