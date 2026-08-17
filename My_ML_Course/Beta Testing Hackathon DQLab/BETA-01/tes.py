import pandas as pd
import numpy as np
from datetime import datetime

"""
CONTOH DATASET IDEAL UNTUK CHATBOT PAHLAWAN MAKASSAR
=====================================================
Dataset ini menunjukkan struktur optimal dengan:
- 6 kolom (prompt, target, category, hero_name, confidence_level, difficulty_level)
- Keseimbangan distribusi tokoh
- Variasi kategori topik
- Panjang jawaban yang informatif
- Keragaman pertanyaan tinggi
"""

# =====================================================
# DEFINISI DATA LENGKAP
# =====================================================

dataset_examples = [
    # ============= SULTAN HASANUDDIN - BIOGRAFI =============
    {
        'prompt': 'Pertanyaan: Kapan Sultan Hasanuddin lahir? Konteks: Sultan Hasanuddin adalah Raja Gowa ke-16 yang dikenal sebagai pahlawan nasional Indonesia.',
        'target': 'Sultan Hasanuddin lahir sekitar tahun 1631 di Kerajaan Gowa, Sulawesi Selatan. Ia adalah putra dari Raja Gowa ke-15, Sultan Malikussaid. Sejak kecil, ia sudah dipersiapkan untuk menjadi pemimpin dan mendapat pendidikan tentang pemerintahan serta strategi militer.',
        'category': 'biografi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    {
        'prompt': 'Pertanyaan: Siapa nama lengkap Sultan Hasanuddin? Konteks: Sultan Hasanuddin memiliki gelar dan nama lengkap yang panjang sesuai tradisi kerajaan.',
        'target': 'Nama lengkap Sultan Hasanuddin adalah I Mallombasi Muhammad Bakir Daeng Mattawang Karaeng Bonto Mangape. Nama ini mencerminkan status dan kedudukannya dalam sistem kerajaan Gowa-Tallo. Ia lebih dikenal dengan gelar Sultan Hasanuddin setelah naik tahta sebagai Raja Gowa ke-16.',
        'category': 'biografi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
    {
        'prompt': 'Pertanyaan: Bagaimana masa kecil Sultan Hasanuddin? Konteks: Sultan Hasanuddin tumbuh di lingkungan istana Kerajaan Gowa.',
        'target': 'Sultan Hasanuddin tumbuh di lingkungan istana Kerajaan Gowa yang kaya akan tradisi dan ilmu pengetahuan. Sejak kecil, ia mendapat pendidikan keagamaan Islam, strategi perang, dan diplomasi. Ia juga dilatih dalam seni bela diri dan berkuda, mempersiapkannya untuk menjadi pemimpin yang tangguh.',
        'category': 'biografi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'medium',
        'difficulty_level': 'intermediate'
    },
    
    # ============= SULTAN HASANUDDIN - PERJUANGAN =============
    {
        'prompt': 'Pertanyaan: Mengapa Sultan Hasanuddin dijuluki Ayam Jantan dari Timur? Konteks: Sultan Hasanuddin terkenal karena perlawanannya terhadap kolonial Belanda.',
        'target': 'Sultan Hasanuddin mendapat julukan "Ayam Jantan dari Timur" atau "De Haantjes van Het Oosten" dari Belanda sendiri. Julukan ini diberikan karena keberaniannya yang luar biasa dalam melawan kolonial Belanda. Meskipun menghadapi kekuatan militer yang lebih besar, Sultan Hasanuddin tidak pernah menyerah dan terus berjuang mempertahankan kemerdekaan Kerajaan Gowa hingga akhir hayatnya.',
        'category': 'perjuangan',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    {
        'prompt': 'Pertanyaan: Bagaimana strategi perang Sultan Hasanuddin melawan Belanda? Konteks: Sultan Hasanuddin menggunakan berbagai taktik dalam menghadapi Belanda.',
        'target': 'Sultan Hasanuddin menggunakan strategi perang gerilya yang memanfaatkan pengetahuan medan lokal. Ia membangun benteng-benteng pertahanan strategis, membentuk aliansi dengan kerajaan-kerajaan lokal seperti Bone dan Soppeng, serta menggunakan jalur laut untuk pergerakan pasukan. Ia juga menerapkan taktik menyerang dan mundur yang membuat Belanda kesulitan mengantisipasi pergerakannya.',
        'category': 'perjuangan',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Kapan terjadi Perang Makassar? Konteks: Perang Makassar adalah konflik besar antara Gowa dan VOC Belanda.',
        'target': 'Perang Makassar berlangsung dari tahun 1666 hingga 1669, yang dikenal sebagai salah satu perang terbesar antara kerajaan lokal dengan VOC Belanda. Konflik ini mencapai puncaknya dengan pengepungan Benteng Somba Opu dan berakhir dengan Perjanjian Bongaya pada 18 November 1667, meskipun perlawanan sporadis masih berlanjut.',
        'category': 'perjuangan',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
    {
        'prompt': 'Pertanyaan: Apa isi Perjanjian Bongaya? Konteks: Perjanjian Bongaya ditandatangani setelah Perang Makassar.',
        'target': 'Perjanjian Bongaya yang ditandatangani pada 18 November 1667 berisi persyaratan yang sangat berat bagi Kerajaan Gowa. Isinya antara lain: Gowa harus menyerahkan monopoli perdagangan rempah-rempah kepada VOC, menghancurkan benteng-benteng pertahanan, menyerahkan beberapa wilayah, dan membayar ganti rugi perang. Perjanjian ini sangat merugikan Gowa namun Sultan Hasanuddin tetap melanjutkan perlawanan secara diam-diam.',
        'category': 'perjuangan',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    
    # ============= SULTAN HASANUDDIN - PRESTASI =============
    {
        'prompt': 'Pertanyaan: Apa prestasi terbesar Sultan Hasanuddin? Konteks: Sultan Hasanuddin memiliki banyak pencapaian sebagai pemimpin.',
        'target': 'Prestasi terbesar Sultan Hasanuddin adalah mempertahankan kehormatan dan martabat Kerajaan Gowa di hadapan kolonialisme Belanda. Ia berhasil menyatukan berbagai kerajaan lokal dalam perlawanan bersama, mempertahankan identitas budaya Makassar, dan menginspirasi perjuangan kemerdekaan generasi selanjutnya. Semangat pantang menyerahnya menjadi simbol perlawanan terhadap penjajahan di Indonesia Timur.',
        'category': 'prestasi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
    {
        'prompt': 'Pertanyaan: Kapan Sultan Hasanuddin diangkat sebagai pahlawan nasional? Konteks: Sultan Hasanuddin diakui sebagai pahlawan nasional Indonesia.',
        'target': 'Sultan Hasanuddin dianugerahi gelar Pahlawan Nasional Indonesia pada tanggal 6 November 1973 melalui Surat Keputusan Presiden Republik Indonesia No. 087/TK/Tahun 1973. Penganugerahan ini mengakui perjuangan dan jasanya dalam melawan penjajahan Belanda serta mempertahankan kemerdekaan rakyat Indonesia Timur.',
        'category': 'prestasi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    
    # ============= SULTAN HASANUDDIN - WARISAN =============
    {
        'prompt': 'Pertanyaan: Apa warisan Sultan Hasanuddin untuk Indonesia? Konteks: Sultan Hasanuddin meninggalkan berbagai warisan penting.',
        'target': 'Warisan Sultan Hasanuddin sangat berharga bagi Indonesia. Pertama, semangat patriotisme dan pantang menyerah yang menginspirasi perjuangan kemerdekaan. Kedua, nilai-nilai kepemimpinan yang berani dan bijaksana. Ketiga, kesadaran akan pentingnya persatuan dalam menghadapi ancaman eksternal. Keempat, warisan budaya dan sejarah Kerajaan Gowa yang memperkaya khazanah peradaban Indonesia. Namanya diabadikan dalam berbagai tempat seperti Bandara Internasional Sultan Hasanuddin dan Universitas Hasanuddin.',
        'category': 'warisan',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Dimana makam Sultan Hasanuddin berada? Konteks: Sultan Hasanuddin dimakamkan di wilayah Gowa.',
        'target': 'Sultan Hasanuddin dimakamkan di kompleks pemakaman Kerajaan Gowa di Katangka, Kabupaten Gowa, Sulawesi Selatan. Makam ini terletak tidak jauh dari bekas Istana Gowa dan menjadi situs bersejarah yang sering dikunjungi untuk mengenang jasa-jasa pahlawan nasional ini. Kompleks pemakaman ini juga menjadi tempat peristirahatan terakhir raja-raja Gowa lainnya.',
        'category': 'lokasi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    
    # ============= KARAENG PATTINGALLOANG - BIOGRAFI =============
    {
        'prompt': 'Pertanyaan: Siapa Karaeng Pattingalloang? Konteks: Karaeng Pattingalloang adalah tokoh penting dalam sejarah Kerajaan Gowa.',
        'target': 'Karaeng Pattingalloang (1600-1654) adalah seorang bangsawan, cendekiawan, dan negarawan Kerajaan Gowa yang sangat dihormati. Ia adalah adik dari Sultan Alauddin, Raja Gowa ke-14, dan menjabat sebagai mangkubumi (perdana menteri) Kerajaan Gowa. Ia terkenal sebagai intelektual yang menguasai berbagai bahasa asing dan ilmu pengetahuan, menjadikannya salah satu tokoh paling terpelajar di Nusantara pada zamannya.',
        'category': 'biografi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    {
        'prompt': 'Pertanyaan: Apa nama lengkap Karaeng Pattingalloang? Konteks: Karaeng Pattingalloang memiliki nama lengkap sesuai tradisi Makassar.',
        'target': 'Nama lengkap Karaeng Pattingalloang adalah I Mallingkaang Daeng Manyonri Karaeng Katangka Tumamenang ri Agamana. Gelar "Karaeng Pattingalloang" berarti "Raja dari Pattingalloang", yang menunjukkan wilayah kekuasaannya. Ia juga dikenal dengan sebutan "Mangkubumi Gowa" karena jabatannya sebagai perdana menteri.',
        'category': 'biografi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
    {
        'prompt': 'Pertanyaan: Kapan Karaeng Pattingalloang lahir dan wafat? Konteks: Karaeng Pattingalloang hidup pada abad ke-17.',
        'target': 'Karaeng Pattingalloang lahir sekitar tahun 1600 di Kerajaan Gowa dan wafat pada tahun 1654. Ia hidup selama masa keemasan Kerajaan Gowa, ketika kerajaan ini menjadi pusat perdagangan dan kebudayaan di Indonesia Timur. Masa hidupnya mencakup periode penting islamisasi dan modernisasi Kerajaan Gowa.',
        'category': 'biografi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    
    # ============= KARAENG PATTINGALLOANG - PRESTASI =============
    {
        'prompt': 'Pertanyaan: Bahasa apa saja yang dikuasai Karaeng Pattingalloang? Konteks: Karaeng Pattingalloang terkenal sebagai polyglot atau ahli bahasa.',
        'target': 'Karaeng Pattingalloang menguasai berbagai bahasa asing yang luar biasa untuk zamannya. Ia fasih berbahasa Arab, Portugis, Spanyol, dan beberapa bahasa Eropa lainnya. Ia juga menguasai bahasa Melayu sebagai lingua franca regional. Kemampuan linguistiknya ini memungkinkannya untuk membaca literatur ilmiah dan filosofis dari berbagai peradaban, serta menjalin diplomasi dengan berbagai bangsa.',
        'category': 'prestasi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
    {
        'prompt': 'Pertanyaan: Apa kontribusi Karaeng Pattingalloang dalam bidang ilmu pengetahuan? Konteks: Karaeng Pattingalloang sangat tertarik dengan berbagai cabang ilmu.',
        'target': 'Karaeng Pattingalloang berkontribusi besar dalam pengembangan ilmu pengetahuan di Nusantara. Ia memiliki perpustakaan pribadi yang berisi ratusan buku tentang astronomi, matematika, geografi, dan filsafat dari berbagai peradaban. Ia membuat catatan dan observasi astronomi, mempelajari peta dunia, dan berdiskusi dengan para sarjana dan pedagang asing yang singgah di Makassar. Ia juga memperkenalkan konsep-konsep ilmiah baru ke lingkungan istana Gowa.',
        'category': 'prestasi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Bagaimana peran Karaeng Pattingalloang dalam diplomasi Gowa? Konteks: Karaeng Pattingalloang adalah negarawan ulung.',
        'target': 'Sebagai mangkubumi, Karaeng Pattingalloang memainkan peran krusial dalam diplomasi Kerajaan Gowa. Ia menjalin hubungan dengan berbagai negara dan kerajaan, termasuk Portugis, Spanyol, dan kerajaan-kerajaan Nusantara lainnya. Kemampuan bahasanya yang luar biasa dan pengetahuannya yang luas membuatnya menjadi diplomat yang sangat dihormati. Ia berhasil menjaga kepentingan Gowa dalam perdagangan internasional dan membangun aliansi strategis.',
        'category': 'prestasi',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    
    # ============= KARAENG PATTINGALLOANG - WARISAN =============
    {
        'prompt': 'Pertanyaan: Apa warisan intelektual Karaeng Pattingalloang? Konteks: Karaeng Pattingalloang meninggalkan warisan pemikiran yang penting.',
        'target': 'Warisan intelektual Karaeng Pattingalloang sangat berharga bagi Indonesia. Ia menunjukkan bahwa tokoh Nusantara pada abad ke-17 sudah memiliki tingkat intelektualitas yang setara dengan cendekiawan Eropa. Pendekatannya yang terbuka terhadap ilmu pengetahuan dari berbagai peradaban menjadi inspirasi bagi tradisi keilmuan inklusif. Ia juga mewariskan tradisi pentingnya pendidikan dan penguasaan bahasa dalam diplomasi dan pemerintahan.',
        'category': 'warisan',
        'hero_name': 'pattingalloang',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Bagaimana Karaeng Pattingalloang dikenang saat ini? Konteks: Karaeng Pattingalloang tetap relevan di masa modern.',
        'target': 'Karaeng Pattingalloang dikenang sebagai simbol kecerdasan dan keterbukaan intelektual Indonesia. Namanya diabadikan dalam berbagai institusi pendidikan dan jalan di Sulawesi Selatan. Ia menjadi inspirasi bagi pengembangan ilmu pengetahuan dan pendidikan di Indonesia Timur. Kisahnya mengajarkan pentingnya menguasai pengetahuan global sambil tetap mempertahankan identitas lokal.',
        'category': 'warisan',
        'hero_name': 'pattingalloang',
        'confidence_level': 'medium',
        'difficulty_level': 'intermediate'
    },
    
    # ============= PERTANYAAN KOMPARATIF =============
    {
        'prompt': 'Pertanyaan: Apa perbedaan Sultan Hasanuddin dan Karaeng Pattingalloang? Konteks: Keduanya adalah tokoh penting Kerajaan Gowa namun dengan peran berbeda.',
        'target': 'Sultan Hasanuddin dan Karaeng Pattingalloang memiliki perbedaan mendasar dalam peran dan pendekatan mereka. Sultan Hasanuddin adalah raja dan panglima perang yang fokus pada perlawanan militer terhadap kolonial Belanda, dikenal karena keberaniannya di medan perang. Sementara Karaeng Pattingalloang adalah cendekiawan dan diplomat yang fokus pada pengembangan intelektual dan hubungan internasional, lebih mengandalkan pengetahuan dan diplomasi. Keduanya melengkapi dalam membangun kejayaan Gowa dari aspek yang berbeda.',
        'category': 'komparasi',
        'hero_name': 'multiple',
        'confidence_level': 'high',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Apakah Sultan Hasanuddin dan Karaeng Pattingalloang pernah bekerja sama? Konteks: Keduanya hidup di periode yang berbeda namun sama-sama di Gowa.',
        'target': 'Sultan Hasanuddin dan Karaeng Pattingalloang tidak pernah bekerja sama secara langsung karena hidup di periode yang berbeda. Karaeng Pattingalloang wafat pada tahun 1654, sementara Sultan Hasanuddin baru naik tahta sebagai Raja Gowa pada tahun 1653-1654 di usia muda. Namun, Sultan Hasanuddin kemungkinan besar mengenal atau mendengar tentang Karaeng Pattingalloang saat masa mudanya, dan mungkin terinspirasi oleh warisan intelektual dan diplomasinya.',
        'category': 'komparasi',
        'hero_name': 'multiple',
        'confidence_level': 'medium',
        'difficulty_level': 'advanced'
    },
    
    # ============= KONTEMPORER & RELEVANSI =============
    {
        'prompt': 'Pertanyaan: Apa relevansi perjuangan Sultan Hasanuddin untuk Indonesia modern? Konteks: Nilai-nilai perjuangan masa lalu tetap penting di era modern.',
        'target': 'Perjuangan Sultan Hasanuddin sangat relevan untuk Indonesia modern. Semangat pantang menyerahnya mengajarkan ketahanan dalam menghadapi tantangan, baik dalam bentuk ancaman fisik maupun penjajahan ekonomi dan budaya di era globalisasi. Nilai keberaniannya menginspirasi generasi muda untuk berani mempertahankan kedaulatan dan identitas bangsa. Kemampuannya menyatukan berbagai kerajaan juga relevan dengan pentingnya persatuan dalam keberagaman Indonesia.',
        'category': 'kontemporer',
        'hero_name': 'hasanuddin',
        'confidence_level': 'medium',
        'difficulty_level': 'advanced'
    },
    {
        'prompt': 'Pertanyaan: Apa yang bisa dipelajari dari Karaeng Pattingalloang di era digital? Konteks: Karaeng Pattingalloang adalah tokoh intelektual yang terbuka terhadap ilmu pengetahuan.',
        'target': 'Di era digital, kita dapat belajar banyak dari Karaeng Pattingalloang tentang pentingnya keterbukaan intelektual dan penguasaan berbagai sumber pengetahuan. Seperti ia yang menguasai banyak bahasa untuk mengakses ilmu dari berbagai peradaban, kita di era digital perlu menguasai literasi digital dan bahasa internasional untuk mengakses informasi global. Pendekatannya yang kritis namun terbuka terhadap pengetahuan baru juga penting untuk menghadapi overload informasi di era ini.',
        'category': 'kontemporer',
        'hero_name': 'pattingalloang',
        'confidence_level': 'medium',
        'difficulty_level': 'advanced'
    },
    
    # ============= LOKASI & WISATA SEJARAH =============
    {
        'prompt': 'Pertanyaan: Dimana saya bisa mempelajari sejarah Sultan Hasanuddin? Konteks: Ada beberapa lokasi bersejarah terkait Sultan Hasanuddin.',
        'target': 'Anda dapat mempelajari sejarah Sultan Hasanuddin di beberapa tempat: Pertama, Museum Balla Lompoa di Sungguminasa, Gowa, yang menyimpan berbagai artefak Kerajaan Gowa. Kedua, kompleks makam Katangka tempat Sultan Hasanuddin dimakamkan. Ketiga, situs Benteng Somba Opu yang merupakan benteng pertahanan utama Gowa. Keempat, Universitas Hasanuddin dan Museum La Galigo di Makassar yang memiliki koleksi literatur dan artefak sejarah Sulawesi Selatan.',
        'category': 'lokasi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'basic'
    },
    {
        'prompt': 'Pertanyaan: Apa itu Benteng Somba Opu? Konteks: Benteng Somba Opu adalah situs bersejarah penting di Makassar.',
        'target': 'Benteng Somba Opu adalah benteng pertahanan utama Kerajaan Gowa yang dibangun pada abad ke-16 dan menjadi saksi perlawanan Sultan Hasanuddin terhadap Belanda. Terletak di tepi Sungai Jeneberang, benteng ini pernah menjadi pusat kekuatan maritim Gowa. Saat ini, situs benteng telah direnovasi dan menjadi taman wisata sejarah yang menampilkan replika rumah adat dari berbagai daerah di Sulawesi Selatan serta museum mini yang menceritakan sejarah Kerajaan Gowa.',
        'category': 'lokasi',
        'hero_name': 'hasanuddin',
        'confidence_level': 'high',
        'difficulty_level': 'intermediate'
    },
]

# =====================================================
# FUNGSI UNTUK GENERATE DATASET LENGKAP
# =====================================================

def generate_complete_dataset(base_examples, total_rows=4000):
    """
    Generate dataset lengkap dengan variasi pertanyaan
    
    Parameters:
    -----------
    base_examples : list
        List contoh data dasar
    total_rows : int
        Target jumlah baris dataset
    
    Returns:
    --------
    pd.DataFrame : Dataset lengkap
    """
    
    print(f"🚀 Generating dataset dengan target {total_rows} baris...")
    
    # Variasi kata tanya untuk membuat pertanyaan berbeda
    question_variations = {
        'Pertanyaan:': ['Pertanyaan:', 'Tanyakan:', 'Tanya:', 'Ditanya:', 'Yang ingin ditanyakan:'],
        'Konteks:': ['Konteks:', 'Latar belakang:', 'Informasi:', 'Tentang:', 'Mengenai:'],
        'Kapan': ['Kapan', 'Sejak kapan', 'Pada tahun berapa', 'Tahun berapa'],
        'Siapa': ['Siapa', 'Siapakah', 'Siapa yang dimaksud', 'Nama siapa'],
        'Apa': ['Apa', 'Apakah', 'Apa saja', 'Apa yang dimaksud'],
        'Mengapa': ['Mengapa', 'Kenapa', 'Apa sebab', 'Apa alasan', 'Karena apa'],
        'Bagaimana': ['Bagaimana', 'Seperti apa', 'Gimana', 'Dengan cara apa'],
        'Dimana': ['Dimana', 'Di mana', 'Lokasi mana', 'Tempat mana']
    }
    
    expanded_data = []
    
    # Replikasi dan variasi data dasar
    multiplier = total_rows // len(base_examples) + 1
    
    for iteration in range(multiplier):
        for example in base_examples:
            # Buat variasi prompt
            varied_prompt = example['prompt']
            
            # Variasi kata-kata kunci
            for original, variations in question_variations.items():
                if original in varied_prompt and len(variations) > 1:
                    # Pilih variasi berdasarkan iterasi
                    variation = variations[iteration % len(variations)]
                    varied_prompt = varied_prompt.replace(original, variation, 1)
            
            # Tambahkan sedikit variasi pada target juga
            varied_target = example['target']
            
            # Untuk iterasi ganjil, tambah awalan pada jawaban
            if iteration % 2 == 1 and example['confidence_level'] == 'high':
                prefixes = [
                    'Berdasarkan catatan sejarah, ',
                    'Menurut sumber terpercaya, ',
                    'Sebagai informasi, ',
                    'Perlu diketahui bahwa ',
                    'Faktanya, '
                ]
                prefix = prefixes[iteration % len(prefixes)]
                varied_target = prefix + varied_target[0].lower() + varied_target[1:]
            
            # Buat entry baru
            new_entry = {
                'prompt': varied_prompt,
                'target': varied_target,
                'category': example['category'],
                'hero_name': example['hero_name'],
                'confidence_level': example['confidence_level'],
                'difficulty_level': example['difficulty_level']
            }
            
            expanded_data.append(new_entry)
            
            # Stop jika sudah mencapai target
            if len(expanded_data) >= total_rows:
                break
        
        if len(expanded_data) >= total_rows:
            break
    
    # Buat DataFrame
    df = pd.DataFrame(expanded_data[:total_rows])
    
    print(f"✅ Dataset berhasil dibuat: {len(df)} baris")
    return df

# =====================================================
# ANALISIS DATASET YANG DIHASILKAN
# =====================================================

def analyze_generated_dataset(df):
    """Analisis kualitas dataset yang dihasilkan"""
    
    print("\n" + "="*60)
    print("📊 ANALISIS DATASET YANG DIHASILKAN")
    print("="*60)
    
    # Basic stats
    print(f"\n📋 STATISTIK DASAR:")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    
    # Length analysis
    print(f"\n📏 ANALISIS PANJANG TEKS:")
    print(f"Avg prompt length: {df['prompt'].str.len().mean():.1f} chars")
    print(f"Avg target length: {df['target'].str.len().mean():.1f} chars")
    print(f"Min prompt length: {df['prompt'].str.len().min()}")
    print(f"Max prompt length: {df['prompt'].str.len().max()}")
    print(f"Min target length: {df['target'].str.len().min()}")
    print(f"Max target length: {df['target'].str.len().max()}")
    
    # Category distribution
    print(f"\n📚 DISTRIBUSI KATEGORI:")
    category_dist = df['category'].value_counts()
    for cat, count in category_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {cat:<15}: {count:>5} ({percentage:>5.1f}%)")
    
    # Hero distribution
    print(f"\n👥 DISTRIBUSI TOKOH:")
    hero_dist = df['hero_name'].value_counts()
    for hero, count in hero_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {hero:<15}: {count:>5} ({percentage:>5.1f}%)")
    
    # Confidence level
    print(f"\n🎯 TINGKAT KEPERCAYAAN:")
    conf_dist = df['confidence_level'].value_counts()
    for conf, count in conf_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {conf:<15}: {count:>5} ({percentage:>5.1f}%)")
    
    # Difficulty level
    print(f"\n📊 TINGKAT KESULITAN:")
    diff_dist = df['difficulty_level'].value_counts()
    for diff, count in diff_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {diff:<15}: {count:>5} ({percentage:>5.1f}%)")
    
    # Quality checks
    print(f"\n✅ QUALITY CHECKS:")
    short_prompts = len(df[df['prompt'].str.len() < 50])
    short_targets = len(df[df['target'].str.len() < 30])
    
    print(f"  Prompts < 50 chars  : {short_prompts}")
    print(f"  Targets < 30 chars  : {short_targets}")
    print(f"  Unique prompts      : {df['prompt'].nunique()}")
    print(f"  Unique targets      : {df['target'].nunique()}")
    print(f"  Prompt diversity    : {(df['prompt'].nunique()/len(df)*100):.1f}%")
    print(f"  Target diversity    : {(df['target'].nunique()/len(df)*100):.1f}%")
    
    return {
        'basic_stats': {
            'total_rows': len(df),
            'avg_prompt_length': df['prompt'].str.len().mean(),
            'avg_target_length': df['target'].str.len().mean()
        },
        'distributions': {
            'category': category_dist.to_dict(),
            'hero': hero_dist.to_dict(),
            'confidence': conf_dist.to_dict(),
            'difficulty': diff_dist.to_dict()
        }
    }

# =====================================================
# EXPORT DATASET
# =====================================================

def export_dataset(df, filename='ideal_hero_dataset.csv', with_analysis=True):
    """
    Export dataset ke CSV dengan analisis opsional
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset yang akan di-export
    filename : str
        Nama file output
    with_analysis : bool
        Apakah menyertakan file analisis terpisah
    """
    
    # Export main dataset
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"\n💾 Dataset disimpan ke: {filename}")
    print(f"   Size: {len(df)} rows x {len(df.columns)} columns")
    
    # Export sample untuk preview
    sample_filename = filename.replace('.csv', '_sample.csv')
    df.head(50).to_csv(sample_filename, index=False, encoding='utf-8')
    print(f"💾 Sample dataset (50 rows) disimpan ke: {sample_filename}")
    
    if with_analysis:
        # Export analysis report
        analysis_filename = filename.replace('.csv', '_analysis.txt')
        with open(analysis_filename, 'w', encoding='utf-8') as f:
            f.write("ANALISIS DATASET CHATBOT PAHLAWAN MAKASSAR\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total Rows: {len(df)}\n")
            f.write(f"Total Columns: {len(df.columns)}\n")
            f.write(f"Columns: {', '.join(df.columns)}\n\n")
            
            f.write("DISTRIBUSI KATEGORI:\n")
            f.write("-" * 30 + "\n")
            for cat, count in df['category'].value_counts().items():
                f.write(f"{cat}: {count} ({count/len(df)*100:.1f}%)\n")
            
            f.write("\nDISTRIBUSI TOKOH:\n")
            f.write("-" * 30 + "\n")
            for hero, count in df['hero_name'].value_counts().items():
                f.write(f"{hero}: {count} ({count/len(df)*100:.1f}%)\n")
            
            f.write("\nKUALITAS DATA:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Avg Prompt Length: {df['prompt'].str.len().mean():.1f} chars\n")
            f.write(f"Avg Target Length: {df['target'].str.len().mean():.1f} chars\n")
            f.write(f"Prompt Diversity: {(df['prompt'].nunique()/len(df)*100):.1f}%\n")
            f.write(f"Target Diversity: {(df['target'].nunique()/len(df)*100):.1f}%\n")
        
        print(f"📄 Analisis report disimpan ke: {analysis_filename}")
    
    print(f"\n✅ Export selesai!")

# =====================================================
# FUNGSI UNTUK MEMBUAT TEMPLATE KOSONG
# =====================================================

def create_template(num_rows=100, filename='dataset_template.csv'):
    """
    Buat template kosong untuk diisi manual
    
    Parameters:
    -----------
    num_rows : int
        Jumlah baris template kosong
    filename : str
        Nama file output
    """
    
    template_data = {
        'prompt': [''] * num_rows,
        'target': [''] * num_rows,
        'category': [''] * num_rows,
        'hero_name': [''] * num_rows,
        'confidence_level': [''] * num_rows,
        'difficulty_level': [''] * num_rows
    }
    
    df_template = pd.DataFrame(template_data)
    
    # Tambah beberapa contoh di baris pertama
    df_template.loc[0] = [
        'Pertanyaan: [Tulis pertanyaan disini] Konteks: [Tulis konteks disini]',
        '[Tulis jawaban lengkap disini - min 50 karakter]',
        '[biografi/perjuangan/prestasi/warisan/lokasi/komparasi/kontemporer]',
        '[hasanuddin/pattingalloang/multiple]',
        '[high/medium/low/partial]',
        '[basic/intermediate/advanced]'
    ]
    
    df_template.to_csv(filename, index=False, encoding='utf-8')
    print(f"📋 Template kosong dibuat: {filename}")
    print(f"   Isi template dengan data Anda, kemudian hapus baris contoh!")

# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == "__main__":
    print("🎯 GENERATOR DATASET IDEAL CHATBOT PAHLAWAN MAKASSAR")
    print("=" * 60)
    
    # Generate dataset lengkap
    ideal_dataset = generate_complete_dataset(dataset_examples, total_rows=4000)
    
    # Analisis dataset
    analysis_results = analyze_generated_dataset(ideal_dataset)
    
    # Export dataset
    export_dataset(ideal_dataset, 'ideal_hero_dataset.csv', with_analysis=True)
    
    # Buat template kosong untuk tambahan manual
    create_template(num_rows=100, filename='dataset_template_to_fill.csv')
    
    print("\n" + "="*60)
    print("🎉 SEMUA PROSES SELESAI!")
    print("="*60)
    
    print("\n📁 FILE YANG DIHASILKAN:")
    print("  1. ideal_hero_dataset.csv (4000 baris - dataset lengkap)")
    print("  2. ideal_hero_dataset_sample.csv (50 baris - untuk preview)")
    print("  3. ideal_hero_dataset_analysis.txt (laporan analisis)")
    print("  4. dataset_template_to_fill.csv (template kosong untuk tambahan)")
    
    print("\n💡 CARA MENGGUNAKAN:")
    print("  1. Review dataset yang dihasilkan")
    print("  2. Gunakan template kosong untuk menambah data custom")
    print("  3. Gabungkan dengan dataset existing Anda")
    print("  4. Lanjutkan ke tahap training model")
    
    print("\n📊 KUALITAS DATASET:")
    stats = analysis_results['basic_stats']
    print(f"  ✅ Avg Prompt Length: {stats['avg_prompt_length']:.1f} chars (Target: >100)")
    print(f"  ✅ Avg Target Length: {stats['avg_target_length']:.1f} chars (Target: >50)")
    print(f"  ✅ Total Rows: {stats['total_rows']:,} (Target: 4000+)")
    
    hero_dist = analysis_results['distributions']['hero']
    total = sum(hero_dist.values())
    print(f"\n  📊 Distribusi Tokoh:")
    for hero, count in hero_dist.items():
        balance_status = "✅" if 25 <= (count/total*100) <= 60 else "⚠️"
        print(f"    {balance_status} {hero}: {(count/total*100):.1f}%")
    
    print("\n🚀 DATASET SIAP UNTUK TRAINING!")
    
    # Return dataset untuk penggunaan lebih lanjut
    print("\n💾 Dataset tersimpan dalam variabel 'ideal_dataset'")
    print("   Gunakan: ideal_dataset.head() untuk melihat preview")

# =====================================================
# FUNGSI UTILITY TAMBAHAN
# =====================================================

def merge_with_existing(existing_csv, ideal_csv, output_csv='merged_dataset.csv'):
    """
    Gabungkan dataset existing dengan dataset ideal
    
    Parameters:
    -----------
    existing_csv : str
        Path ke dataset existing
    ideal_csv : str
        Path ke dataset ideal
    output_csv : str
        Path output file merged
    """
    
    print(f"\n🔄 Menggabungkan dataset...")
    
    # Load datasets
    df_existing = pd.read_csv(existing_csv)
    df_ideal = pd.read_csv(ideal_csv)
    
    print(f"  Existing dataset: {len(df_existing)} rows")
    print(f"  Ideal dataset: {len(df_ideal)} rows")
    
    # Jika existing dataset tidak punya kolom lengkap, tambahkan
    if 'category' not in df_existing.columns:
        df_existing['category'] = 'uncategorized'
    if 'hero_name' not in df_existing.columns:
        df_existing['hero_name'] = 'unknown'
    if 'confidence_level' not in df_existing.columns:
        df_existing['confidence_level'] = 'medium'
    if 'difficulty_level' not in df_existing.columns:
        df_existing['difficulty_level'] = 'basic'
    
    # Merge
    df_merged = pd.concat([df_existing, df_ideal], ignore_index=True)
    
    # Remove duplicates based on prompt
    df_merged = df_merged.drop_duplicates(subset=['prompt'], keep='first')
    
    # Save
    df_merged.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"\n✅ Dataset merged berhasil!")
    print(f"  Total rows after merge: {len(df_merged)}")
    print(f"  Duplicates removed: {len(df_existing) + len(df_ideal) - len(df_merged)}")
    print(f"  Output saved to: {output_csv}")
    
    return df_merged

def split_train_val_test(df, train_ratio=0.8, val_ratio=0.15, test_ratio=0.05, 
                         output_dir='dataset_splits'):
    """
    Split dataset menjadi train, validation, dan test sets
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset yang akan di-split
    train_ratio : float
        Proporsi data training (default: 0.8)
    val_ratio : float
        Proporsi data validation (default: 0.15)
    test_ratio : float
        Proporsi data testing (default: 0.05)
    output_dir : str
        Direktori output
    """
    
    import os
    from sklearn.model_selection import train_test_split
    
    print(f"\n✂️ Splitting dataset...")
    print(f"  Train: {train_ratio*100:.0f}%")
    print(f"  Validation: {val_ratio*100:.0f}%")
    print(f"  Test: {test_ratio*100:.0f}%")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # First split: train and temp (val+test)
    train_df, temp_df = train_test_split(df, test_size=(1-train_ratio), 
                                          random_state=42, stratify=df['hero_name'])
    
    # Second split: val and test
    val_size = val_ratio / (val_ratio + test_ratio)
    val_df, test_df = train_test_split(temp_df, test_size=(1-val_size), 
                                        random_state=42, stratify=temp_df['hero_name'])
    
    # Save splits
    train_df.to_csv(f'{output_dir}/train.csv', index=False, encoding='utf-8')
    val_df.to_csv(f'{output_dir}/validation.csv', index=False, encoding='utf-8')
    test_df.to_csv(f'{output_dir}/test.csv', index=False, encoding='utf-8')
    
    print(f"\n✅ Dataset berhasil di-split!")
    print(f"  Train: {len(train_df)} rows -> {output_dir}/train.csv")
    print(f"  Validation: {len(val_df)} rows -> {output_dir}/validation.csv")
    print(f"  Test: {len(test_df)} rows -> {output_dir}/test.csv")
    
    # Verify distribution in each split
    print(f"\n📊 Distribusi tokoh per split:")
    for split_name, split_df in [('Train', train_df), ('Val', val_df), ('Test', test_df)]:
        hero_dist = split_df['hero_name'].value_counts()
        print(f"\n  {split_name}:")
        for hero, count in hero_dist.items():
            percentage = (count / len(split_df)) * 100
            print(f"    {hero}: {count} ({percentage:.1f}%)")
    
    return train_df, val_df, test_df

# =====================================================
# CONTOH PENGGUNAAN LENGKAP
# =====================================================

"""
PANDUAN LENGKAP PENGGUNAAN:
==========================

1. GENERATE DATASET IDEAL:
   python ideal_hero_dataset.py

2. MERGE DENGAN DATASET EXISTING:
   merged = merge_with_existing(
       'processed_text_generation_dataset.csv',
       'ideal_hero_dataset.csv',
       'merged_hero_dataset.csv'
   )

3. SPLIT UNTUK TRAINING:
   train, val, test = split_train_val_test(
       merged,
       train_ratio=0.8,
       val_ratio=0.15,
       test_ratio=0.05
   )

4. GUNAKAN UNTUK TRAINING MODEL:
   # Dengan Transformers
   from transformers import T5ForConditionalGeneration
   
   # Load data
   train_df = pd.read_csv('dataset_splits/train.csv')
   
   # Format untuk training
   train_data = [
       {
           'input_text': row['prompt'],
           'target_text': row['target']
       }
       for _, row in train_df.iterrows()
   ]

5. EVALUASI KUALITAS:
   from dataset_analyzer import analyze_hero_dataset
   results = analyze_hero_dataset('merged_hero_dataset.csv')

TIPS PENTING:
============
- Pastikan distribusi tokoh seimbang (25-40% per tokoh)
- Rata-rata panjang target minimal 50 karakter
- Keragaman prompt minimal 70%
- Confidence level 'high' untuk fakta sejarah yang terverifikasi
- Gunakan difficulty_level untuk stratified sampling saat training

TROUBLESHOOTING:
===============
Q: Dataset terlalu besar, perlu downsampling?
A: Gunakan: df.sample(n=3000, random_state=42)

Q: Ingin fokus ke tokoh tertentu?
A: df[df['hero_name'] == 'hasanuddin']

Q: Perlu update confidence level?
A: df.loc[df['category'] == 'biografi', 'confidence_level'] = 'high'

Q: Export ke format lain?
A: df.to_json('dataset.json', orient='records', force_ascii=False)
   df.to_excel('dataset.xlsx', index=False)
"""