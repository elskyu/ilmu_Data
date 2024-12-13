from inertia import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from efficient_apriori import apriori

def home(request):
    file_path = './excel/pizza_sales2.csv'
    try:
        # Membaca file CSV
        print(f"Mencoba membaca file dari {file_path}")
        data = pd.read_csv(file_path)
        dataitem = data.drop(['pizza_size', 'unit_price', 'pizza_id', 'pizza_name_id', 'quantity', 'order_date', 'order_time', 'total_price', 'pizza_category', 'pizza_ingredients'], axis=1)
        dataitem = dataitem.groupby('order_id').agg(",".join).reset_index()
        dataitem = dataitem.drop(['order_id'], axis=1)
        records = []
        for i in range(dataitem.shape[0]):
            records.append([str(dataitem.values[i, j]).split(',') for j in range(dataitem.shape[1])])
        act = [[] for _ in range(len(records))]
        for i in range(len(records)):
            for j in records[i][0]:
                act[i].append(j)

        # Menjalankan algoritma apriori
        print("Menjalankan algoritma apriori...")
        itemsets, rules = apriori(act, min_confidence=0.1, min_support=0.01)
        print(f"Jumlah aturan asosiasi yang ditemukan: {len(rules)}")
        if not rules:
            print("Tidak ada aturan asosiasi yang ditemukan.")
        rules_rhs_1 = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 1, rules)
        association_rules_1 = [str(rule) for rule in sorted(rules_rhs_1, key=lambda rule: rule.lift, reverse=True)]
        rules_rhs_2 = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
        association_rules_2 = [str(rule) for rule in sorted(rules_rhs_2, key=lambda rule: rule.lift, reverse=True)]
        print(f"Jumlah aturan asosiasi dengan presedence 1: {len(association_rules_1)}")
        print(f"Jumlah aturan asosiasi dengan presedence 2: {len(association_rules_2)}")

        # Mengambil input 'item' dari query parameter untuk filter aturan asosiasi
        item = request.GET.get('item', '').lower()  
        if item:
            filtered_rules = [rule for rule in association_rules_1 + association_rules_2 if item in rule.lower()]
            print(f"Jumlah aturan asosiasi setelah filter berdasarkan item '{item}': {len(filtered_rules)}")
        else:
            filtered_rules = association_rules_1 + association_rules_2

        # Menghitung frequent itemsets (k1 dan k2)
        print("Menghitung frequent itemsets (k1 dan k2)...")
        k1 = itemsets[1] if 1 in itemsets else {}
        k2 = itemsets[2] if 2 in itemsets else {}

        # Menyusun k1 dan k2 sebagai list untuk dikirim ke frontend
        k1_list = [{"item": key, "support": value} for key, value in k1.items()]
        k2_list = [{"item_pair": key, "support": value} for key, value in k2.items()]
        fig, ax = plt.subplots(figsize=(8, 8))

        data['pizza_category'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')
        img_buf.seek(0)
        chart_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')
        df = data.fillna(value=0)  
        pokedex_data = df.to_dict(orient='records')

        # Kirim data ke Vue.js menggunakan Inertia.js
        return render(request, 'Home', props={
            'title': 'DATASET PIZZA',
            'description': 'Berikut merupakan tabel dari dataset penjualan pizza :',
            'deskripsi': 'Berikut merupakan visualisasi dari tabel di atas :',
            'pokedex': pokedex_data,
            'grafik': 'Visualisasi Data',
            'chart_data': chart_data,  
            'association_rules': filtered_rules,  
            'k1': k1_list,  
            'k2': k2_list   
        })

    except FileNotFoundError:
        # Jika file tidak ditemukan, kirim data kosong
        print(f"File tidak ditemukan di {file_path}")
        pokedex_data = []
        chart_data = None
        association_rules = []
        return render(request, 'Home', props={
            'title': 'DATASET PIZZA',
            'description': 'Berikut merupakan tabel dari dataset penjualan pizza :',
            'deskripsi': 'Berikut merupakan visualisasi dari tabel di atas :',
            'pokedex': pokedex_data,
            'grafik': 'VISUALISASI DATA',
            'chart_data': chart_data,
            'association_rules': association_rules, 
            'k1': [],  
            'k2': [] 
        })