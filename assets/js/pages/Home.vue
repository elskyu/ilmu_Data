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
        association_rules: Array,
        k1: Array,
        k2: Array,
    },
    data() {
        return {
            searchItem: '', // Input pengguna
            filteredRules: [], // Menyimpan aturan asosiasi yang difilter
            currentPageRules: 1, // Halaman saat ini untuk asosiasi
            rulesPerPage: 5, // Batas jumlah aturan per halaman
            currentPageK1: 1,
            currentPageK2: 1,
            itemsPerPage: 5,
        };
    },
    computed: {
        paginatedRules() {
            const startIndex = (this.currentPageRules - 1) * this.rulesPerPage;
            const endIndex = startIndex + this.rulesPerPage;
            return this.filteredRules.slice(startIndex, endIndex);
        },
        totalPagesRules() {
            return Math.ceil(this.filteredRules.length / this.rulesPerPage);
        },
        paginatedK1() {
            const startIndex = (this.currentPageK1 - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            return this.k1.slice(startIndex, endIndex);
        },
        totalPagesK1() {
            return Math.ceil(this.k1.length / this.itemsPerPage);
        },
        paginatedK2() {
            const startIndex = (this.currentPageK2 - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            return this.k2.slice(startIndex, endIndex);
        },
        totalPagesK2() {
            return Math.ceil(this.k2.length / this.itemsPerPage);
        },
    },
    methods: {
        searchAssociation() {
            if (this.searchItem.trim() !== '') {
                this.filteredRules = this.association_rules.filter(rule =>
                    rule.toLowerCase().includes(this.searchItem.toLowerCase())
                );
            } else {
                this.filteredRules = [];
            }
            this.currentPageRules = 1;
        },
        prevPage() {
            if (this.currentPageRules > 1) {
                this.currentPageRules--;
            }
        },
        nextPage() {
            if (this.currentPageRules < this.totalPagesRules) {
                this.currentPageRules++;
            }
        },
        prevPageK1() {
            if (this.currentPageK1 > 1) {
                this.currentPageK1--;
            }
        },
        nextPageK1() {
            if (this.currentPageK1 < this.totalPagesK1) {
                this.currentPageK1++;
            }
        },
        prevPageK2() {
            if (this.currentPageK2 > 1) {
                this.currentPageK2--;
            }
        },
        nextPageK2() {
            if (this.currentPageK2 < this.totalPagesK2) {
                this.currentPageK2++;
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
                    <img src="./pizza_bg6.png" alt="Pizza Background" class="responsive-img" loading="lazy">
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
                                        <th>Aturan Asosiasi</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(rule, index) in paginatedRules" :key="index">
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

                <!-- Card Frequent Itemsets K1 -->
                <div id="frequent-k1" class="section card">
                    <h3>Frekuensi K1</h3>
                    <div v-if="paginatedK1 && paginatedK1.length">
                        <table class="association-table">
                            <thead>
                                <tr>
                                    <th>Frequent Item</th>
                                    <th>Frekuensi</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in paginatedK1" :key="index">
                                    <td>{{ item.item }}</td>
                                    <td>{{ item.support }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-else>
                        <p>No frequent itemsets K1 available.</p>
                    </div>

                    <!-- Navigasi Halaman -->
                    <div class="pagination-controls">
                        <button @click="prevPageK1" :disabled="currentPageK1 === 1">Previous</button>
                        <span>Page {{ currentPageK1 }} of {{ totalPagesK1 }}</span>
                        <button @click="nextPageK1" :disabled="currentPageK1 === totalPagesK1">Next</button>
                    </div>
                </div>

                <!-- Card Frequent Itemsets K2 -->
                <div id="frequent-k2" class="section card">
                    <h3>Frekuensi K2</h3>
                    <div v-if="paginatedK2 && paginatedK2.length">
                        <table class="association-table">
                            <thead>
                                <tr>
                                    <th>Item Pair</th>
                                    <th>Frekuensi</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in paginatedK2" :key="index">
                                    <td>{{ item.item_pair }}</td>
                                    <td>{{ item.support }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-else>
                        <p>No frequent itemsets K2 available.</p>
                    </div>

                    <!-- Navigasi Halaman -->
                    <div class="pagination-controls">
                        <button @click="prevPageK2" :disabled="currentPageK2 === 1">Previous</button>
                        <span>Page {{ currentPageK2 }} of {{ totalPagesK2 }}</span>
                        <button @click="nextPageK2" :disabled="currentPageK2 === totalPagesK2">Next</button>
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

<style scoped></style>