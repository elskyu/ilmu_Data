from inertia import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def home(request):
    # Path ke file Excel
    file_path = './excel/restaurant2.xlsx'
    
    try:
        # Membaca file Excel
        df = pd.read_excel(file_path)
        
        # Menghitung jumlah peserta untuk setiap baris
        # Mengasumsikan 'Participants' adalah string dengan nama peserta yang dipisahkan oleh spasi
        df['Participants'] = df['Participants'].apply(lambda x: str(x).strip('[]').replace('"', '').split(' '))  # Membersihkan tanda `[` dan `"`

        # Agregasi data berdasarkan 'Type of Meal' dan menghitung total participants per meal type
        meal_participants = df.groupby('Type of Meal')['Participants'].sum().reset_index()

        # Membuat diagram pie
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(meal_participants['Participants'].apply(len),  # Jumlah peserta per type of meal
               labels=meal_participants['Type of Meal'], 
               autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)

        # Menyimpan gambar pie chart ke dalam buffer
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Mengonversi gambar menjadi format base64
        chart_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

        # Menyusun data untuk Vue.js
        df = df.fillna(value=0)  # Jika ingin mengganti NaN dengan angka 0
        pokedex_data = df.to_dict(orient='records')

    except FileNotFoundError:
        pokedex_data = []
        chart_data = None  # Jika file tidak ditemukan, tidak ada chart yang dikirimkan

    # Kirim data ke Vue.js menggunakan Inertia.js
    return render(request, 'Home', props={
        'title': 'DATASET RESTORAN',
        'description': 'Berikut merupakan tabel dari dataset restoran :',
        'deskripsi' : 'Berikut merupakan visualisasi dari tabel diatas :',
        'pokedex': pokedex_data,
        'grafik': 'VISUALISASI DATA',
        'chart_data': chart_data  # Pastikan chart_data dikirim ke frontend
    })
