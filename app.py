from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# SQL VERİTABANI BAĞLANTISI VE TABLO OLUŞTURMA
def veritabani_hazirla():
    conn = sqlite3.connect('veritabani.db')
    cursor = conn.cursor()
    # Eğer tablo yoksa otomatik oluşturur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesajlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icerik TEXT NOT NULL,
            tarih TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 1. SAYFAYI GÖRÜNTÜLEME VE SQL'DEN VERİ OKUMA
@app.route('/')
def ana_sayfa():
    conn = sqlite3.connect('veritabani.db')
    cursor = conn.cursor()
    # Mesajları tarihe göre yeniden eskiye sıralayarak çeker
    cursor.execute('SELECT * FROM mesajlar ORDER BY id DESC')
    tum_mesajlar = cursor.fetchall()
    conn.close()
    return render_template('index.html', mesajlar=tum_mesajlar)

# 2. SQL VERİTABANINA YAZMA (YAYINLA BUTONU)
@app.route('/gonder', methods=['POST'])
def mesaj_gonder():
    mesaj_txt = request.form.get('mesaj icerik')
    if mesaj_txt and mesaj_txt.strip() != "":
        su_an = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        # Veritabanına ekleme işlemi (SQL INSERT)
        conn = sqlite3.connect('veritabani.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mesajlar (icerik, tarih) VALUES (?, ?)', (mesaj_txt.strip(), su_an))
        conn.commit()
        conn.close()
        
    return redirect('/')

if __name__ == '__main__':
    veritabani_hazirla() # İlk açılışta SQL tablosunu kurar
    app.run(debug=True)