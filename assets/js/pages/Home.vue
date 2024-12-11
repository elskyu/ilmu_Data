<script>
import './style.css';

export default {
    props: {
        grafik: String,
        title: String,
        description: String,
        deskripsi: String,
        pokedex: Array,
        chart_data: String,
        chart_data_2: String,
        currentPage: Number,
        totalPages: Number,
        association_rules: Array, // Semua aturan asosiasi
    },
    data() {
        return {
            searchItem: '', // Input pengguna
            filteredRules: [], // Menyimpan aturan asosiasi yang difilter
            currentPageRules: 1, // Halaman saat ini untuk asosiasi
            rulesPerPage: 5, // Batas jumlah aturan per halaman
        };
    },
    computed: {
        // Aturan yang ditampilkan berdasarkan halaman saat ini
        paginatedRules() {
            const startIndex = (this.currentPageRules - 1) * this.rulesPerPage;
            const endIndex = startIndex + this.rulesPerPage;
            return this.filteredRules.slice(startIndex, endIndex);
        },
        // Total halaman berdasarkan jumlah aturan
        totalPagesRules() {
            return Math.ceil(this.filteredRules.length / this.rulesPerPage);
        },
    },
    methods: {
        // Menyaring asosiasi berdasarkan input pengguna
        searchAssociation() {
            if (this.searchItem.trim() !== '') {
                this.filteredRules = this.association_rules.filter(rule =>
                    rule.toLowerCase().includes(this.searchItem.toLowerCase())
                );
            } else {
                this.filteredRules = [];
            }
            this.currentPageRules = 1; // Reset ke halaman pertama
        },
        // Navigasi ke halaman sebelumnya
        prevPage() {
            if (this.currentPageRules > 1) {
                this.currentPageRules--;
            }
        },
        // Navigasi ke halaman berikutnya
        nextPage() {
            if (this.currentPageRules < this.totalPagesRules) {
                this.currentPageRules++;
            }
        },
    },
};
</script>

<template>
    <div class="main-container">
        <div class="login-wrapper">
            <div id="main-content" class="main-content">
                <!-- Gambar -->
                <div class="image-wrapper">
                    <img src="./pizza_bg6.png" alt="Pizza Background" class="responsive-img">
                </div>

                <!-- Tabel Data - Card Wrapper -->
                <div id="tabel" class="section card">
                    <h3>Tabel Data Pizza</h3>
                    <div v-if="!pokedex || pokedex.length === 0">
                        <p>No items available</p>
                    </div>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th v-for="(value, key) in pokedex[0]" :key="key">{{ key }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, index) in pokedex" :key="index">
                                    <td v-for="(value, key) in row" :key="key">{{ value || '-' }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Wrapper untuk Grafik dan Asosiasi -->
                <div class="flex-container">
                    <!-- Grafik -->
                    <div id="grafik" class="section card flex-item">
                        <h3>{{ grafik }}</h3>
                        <div class="chart-wrapper">
                            <img :src="'data:image/png;base64,' + chart_data" alt="Pie Chart" class="chart-img" />
                        </div>
                    </div>


                    <div id="asosiasi" class="section card flex-item">
                        <h3>Aturan Asosiasi</h3>
                        <!-- Input untuk menyaring aturan asosiasi -->
                        <div class="input-association">
                            <div class="form-group">
                                <input type="text" id="itemInput" v-model="searchItem" @input="searchAssociation"
                                    placeholder="Masukkan nama item..." class="form-input" />
                                <button @click="searchAssociation" class="form-button">Cari</button>
                            </div>
                        </div>

                        <!-- Menampilkan aturan asosiasi dalam tabel -->
                        <div v-if="paginatedRules && paginatedRules.length">
                            <table class="association-table">
                                <thead>
                                    <tr>
                                        <th>No</th>
                                        <th>Aturan Asosiasi</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(rule, index) in paginatedRules" :key="index">
                                        <td>{{ (currentPageRules - 1) * rulesPerPage + index + 1
                                            }}</td>
                                        <td>{{ rule }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else>
                            <p>No association rules available for the entered item.</p>
                        </div>

                        <!-- Navigasi Halaman -->
                        <div class="pagination-controls">
                            <button @click="prevPage" :disabled="currentPageRules === 1">Previous</button>
                            <span>Page {{ currentPageRules }} of {{ totalPagesRules }}</span>
                            <button @click="nextPage" :disabled="currentPageRules === totalPagesRules">Next</button>
                        </div>
                    </div>
                </div>

                <!-- Footer Section -->
                <footer class="footer">
                    <a>@develop in Desember 2024</a>
                </footer>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Tabel untuk aturan asosiasi */
.association-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 14px;
}

.association-table th,
.association-table td {
    border: 1px solid #dddddd;
    text-align: center;
    padding: 10px;
    word-wrap: break-word;
}

.association-table th {
    background-color: rgb(249, 207, 177);
    color: white;
    font-weight: bold;
}

.association-table tr:nth-child(even) {
    background-color: #f9f9f9;
}

.association-table tr:hover {
    background-color: #f1f1f1;
}

.association-table th:nth-child(1),
.association-table td:nth-child(1) {
    width: 25%;
}

.association-table th:nth-child(2),
.association-table td:nth-child(2) {
    width: 75%;
}
</style>