<template>
    <div class="container">
        <!-- Sidebar Atas (Judul) -->
        <div class="sidebar-top">
            <h2>Data Science</h2>
        </div>

        <!-- Sidebar Bawah (Menu) -->
        <div class="sidebar-bottom">
            <ul>
                <li><a href="#main-content">Tabel</a></li>
                <li><a href="#grafik">Grafik</a></li>
            </ul>
        </div>

        <!-- Main Content -->
        <div id="main-content" class="main-content">

            <!-- Tabel Data - Card Wrapper -->
            <div id="tabel" class="section card">
                <h3>Tabel Data Restoran</h3>
                <table v-if="pokedex && pokedex.length">
                    <tbody>
                        <tr>
                            <!-- Kolom untuk Nomor Urut -->
                            <th>No.</th>
                            <th v-for="(value, key) in pokedex[0]" :key="key">{{ key }}</th>
                        </tr>
                        <tr v-for="(row, index) in pokedex" :key="index">
                            <!-- Nomor Urut -->
                            <td>{{ index + 1 }}</td>
                            <td v-for="(value, key) in row" :key="key">{{ value }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Visualisasi Grafik - Card Wrapper -->
            <div id="grafik" class="section card">
                <h3>{{ grafik }}</h3>

                <!-- Layout Flexbox untuk Menampilkan Dua Grafik -->
                <div class="charts-container">
                    <!-- Menampilkan Grafik Pie Chart 1 -->
                    <div v-if="chart_data" class="chart">
                        <img :src="'data:image/png;base64,' + chart_data" alt="Pie Chart 1"
                            style="width: 100%; height: auto; display: block; margin: 0 auto; margin-bottom: 50px; margin-top: 10px; border: 1px solid #000000;">
                    </div>
                    <div v-else>
                        <p>No chart 1 available</p>
                    </div>

                    <!-- Menampilkan Grafik Pie Chart 2 -->
                    <div v-if="chart_data" class="chart">
                        <img :src="'data:image/png;base64,' + chart_data" alt="Pie Chart 2"
                            style="width: 100%; height: auto; display: block; margin: 0 auto; margin-bottom: 50px; margin-top: 10px; border: 1px solid #000000;">
                    </div>
                    <div v-else>
                        <p>No chart 2 available</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        grafik: String,          // Judul grafik
        title: String,           // Judul halaman
        description: String,     // Deskripsi halaman
        deskripsi: String,       // Deskripsi grafik
        pokedex: Array,          // Data untuk tabel
        chart_data: String,      // Data base64 untuk grafik pertama
        chart_data_2: String,    // Data base64 untuk grafik kedua
        currentPage: Number,     // Halaman saat ini
        totalPages: Number       // Total halaman untuk paginasi
    }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap');

.container {
    display: flex;
}

.sidebar-top {
    width: 200px;
    background-color: #17818f;
    color: white;
    padding: 20px;
    height: 5vh;
    position: fixed;
    top: 0;
    left: 0;
    font-family: 'Quicksand', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
}

.sidebar-top h2 {
    margin: 0;
    font-size: 1.5em;
}

.sidebar-bottom {
    width: 200px;
    height: 83vh;
    background-color: #17818f;
    color: white;
    padding: 20px;
    position: fixed;
    bottom: 0;
    left: 0;
    font-family: 'Quicksand', sans-serif;
}

.sidebar-bottom ul {
    list-style: none;
    padding: 0;
}

.sidebar-bottom ul li {
    margin: 15px 0;
}

.sidebar-bottom ul li a {
    color: white;
    text-decoration: none;
    font-size: 1.2em;
}

.sidebar-bottom ul li a:hover {
    text-decoration: underline;
}

.main-content {
    margin-left: 260px;
    width: calc(100% - 250px);
    padding: 20px;
    margin-bottom: 80px;
}

h1 {
    text-align: center;
    font-size: 2em;
    font-family: 'Quicksand', sans-serif;
    margin-bottom: -10px;
}

p {
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.2em;
    color: #000000;
    font-family: 'Quicksand', sans-serif;
}

table {
    width: 100%;
    border-collapse: separate;
    margin: 0 auto;
    font-family: 'Quicksand', sans-serif;
}

th {
    border: 1px solid #000000;
    overflow: hidden;
    font-size: 8pt;
}

td {
    text-align: center;
    border: 1px solid #000000;
    overflow: hidden;
    padding: 10px;
    font-size: 8pt;
}

th {
    background-color: #17818f;
    text-align: center;
    color: white;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

tbody {
    display: block;
    max-height: 560px;
    overflow-y: auto;
    border: 1px solid #000000;
}

thead tr {
    display: table;
    width: 100%;
    height: 50px;
}

tbody tr {
    display: table;
    width: 100%;
    table-layout: fixed;
    height: 50px;
}

/* Layout untuk dua grafik */
.charts-container {
    display: flex;
    justify-content: space-around;
    margin-top: 25px;
}

.chart {
    width: 45%;
}

/* Styling untuk section (Tabel dan Grafik) agar ada jarak antar bagian */
.section {
    margin-top: px;
}

/* Styling untuk Card */
.card {
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
    padding: 20px;
    margin-bottom: 30px;
}

.card h3 {
    text-align: center;
    font-size: 1.5em;
    margin-bottom: 5px;
    font-family: 'Quicksand', sans-serif;
}

/* Sidebar Atas (Judul) */
.sidebar-top {
    width: 200px;
    background-color: #17818f;
    color: white;
    padding: 20px;
    height: 5vh;
    position: fixed;
    margin-left: 10px;
    margin-top: 20px;
    top: 0;
    left: 0;
    font-family: 'Quicksand', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
    /* Shadow effect */
}

.sidebar-top h2 {
    margin: 0;
    font-size: 1.5em;
}

/* Sidebar Bawah (Menu) */
.sidebar-bottom {
    width: 200px;
    height: 77vh;
    background-color: #17818f;
    color: white;
    padding: 20px;
    position: fixed;
    bottom: 0;
    left: 0;
    margin-left: 10px;
    margin-top: 10px;
    margin-bottom: 20px;
    font-family: 'Quicksand', sans-serif;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
    /* Shadow effect */
}

.sidebar-bottom ul {
    list-style: none;
    padding: 0;
}

.sidebar-bottom ul li {
    margin: 15px 0;
}

.sidebar-bottom ul li a {
    color: white;
    text-decoration: none;
    font-size: 1.2em;
}

.sidebar-bottom ul li a:hover {
    text-decoration: underline;
}
</style>
