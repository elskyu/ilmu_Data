from inertia import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from efficient_apriori import apriori

def home(request):
    # Path ke file dataset CSV
    file_path = './excel/pizza_sales2.csv'
    
    try:
        # Membaca file CSV
        print(f"Mencoba membaca file dari {file_path}")
        data = pd.read_csv(file_path)

        # Memilih kolom yang diperlukan dan membuang kolom yang tidak relevan
        dataitem = data.drop(['pizza_size', 'unit_price', 'pizza_id', 'pizza_name_id', 'quantity', 'order_date', 'order_time', 'total_price', 'pizza_category', 'pizza_ingredients'], axis=1)

        # Menggabungkan data berdasarkan 'order_id' dan menggabungkan isi setiap kolom
        dataitem = dataitem.groupby('order_id').agg(",".join).reset_index()

        # Menghapus 'order_id' karena tidak diperlukan untuk transaksi
        dataitem = dataitem.drop(['order_id'], axis=1)

        # Mengonversi data menjadi list transaksi
        records = []
        for i in range(dataitem.shape[0]):
            records.append([str(dataitem.values[i, j]).split(',') for j in range(dataitem.shape[1])])

        # Menyusun transaksi menjadi list individual
        act = [[] for _ in range(len(records))]
        for i in range(len(records)):
            for j in records[i][0]:
                act[i].append(j)

        # Menjalankan algoritma apriori
        print("Menjalankan algoritma apriori...")
        itemsets, rules = apriori(act, min_confidence=0.1, min_support=0.01)

        # Debugging: Tampilkan jumlah aturan asosiasi yang ditemukan
        print(f"Jumlah aturan asosiasi yang ditemukan: {len(rules)}")
        if not rules:
            print("Tidak ada aturan asosiasi yang ditemukan.")

        # Menyaring aturan asosiasi dengan presedence 1
        rules_rhs_1 = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 1, rules)
        association_rules_1 = [str(rule) for rule in sorted(rules_rhs_1, key=lambda rule: rule.lift, reverse=True)]

        # Menyaring aturan asosiasi dengan presedence 2
        rules_rhs_2 = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
        association_rules_2 = [str(rule) for rule in sorted(rules_rhs_2, key=lambda rule: rule.lift, reverse=True)]

        # Debugging: Tampilkan jumlah aturan setelah penyaringan
        print(f"Jumlah aturan asosiasi dengan presedence 1: {len(association_rules_1)}")
        print(f"Jumlah aturan asosiasi dengan presedence 2: {len(association_rules_2)}")

        # Mengambil input 'item' dari query parameter untuk filter aturan asosiasi
        item = request.GET.get('item', '').lower()  # Dapatkan item dari request GET
        if item:
            # Filter aturan asosiasi berdasarkan item yang diberikan
            filtered_rules = [rule for rule in association_rules_1 + association_rules_2 if item in rule.lower()]
            print(f"Jumlah aturan asosiasi setelah filter berdasarkan item '{item}': {len(filtered_rules)}")
        else:
            filtered_rules = association_rules_1 + association_rules_2

        # Membuat grafik pie chart berdasarkan data (misalnya berdasarkan 'pizza_category' atau kolom lainnya)
        fig, ax = plt.subplots(figsize=(8, 8))
        data['pizza_category'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        
        # Menyimpan grafik pie chart ke dalam buffer
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Mengonversi grafik menjadi format base64
        chart_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')

        # Menyusun data untuk Vue.js
        df = data.fillna(value=0)  # Mengganti NaN dengan 0
        pokedex_data = df.to_dict(orient='records')

        # Kirim data ke Vue.js menggunakan Inertia.js
        return render(request, 'Home', props={
            'title': 'DATASET PIZZA',
            'description': 'Berikut merupakan tabel dari dataset penjualan pizza :',
            'deskripsi': 'Berikut merupakan visualisasi dari tabel di atas :',
            'pokedex': pokedex_data,
            'grafik': 'Visualisasi Data',
            'chart_data': chart_data,  # Pastikan chart_data dikirim ke frontend
            'association_rules': filtered_rules  # Kirimkan aturan asosiasi yang telah difilter
        })

    except FileNotFoundError:
        # Jika file tidak ditemukan, kirim data kosong
        print(f"File tidak ditemukan di {file_path}")
        pokedex_data = []
        chart_data = None  # Tidak ada chart yang dikirimkan
        association_rules = []  # Tidak ada aturan asosiasi jika file tidak ditemukan

        # Kirim data ke Vue.js menggunakan Inertia.js
        return render(request, 'Home', props={
            'title': 'DATASET PIZZA',
            'description': 'Berikut merupakan tabel dari dataset penjualan pizza :',
            'deskripsi': 'Berikut merupakan visualisasi dari tabel di atas :',
            'pokedex': pokedex_data,
            'grafik': 'VISUALISASI DATA',
            'chart_data': chart_data,  # Pastikan chart_data dikirim ke frontend
            'association_rules': association_rules  # Kirimkan aturan asosiasi kosong
        })
