Nama: Aulia Nur Shiva

NPM: 2506619316

Kelas: PBP A

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti < section > dan < details > dalam membuat web portofolio saya. < section > membantu saya membagi halaman menjadi beberapa bagian yang jelas, seperti profile, experiences, dan interest. sementara itu, saya menggunakan < details > untuk membuat informasi pada bagian experiences dan interest dapat dibuka dan ditutup

2. Tantangan yang saya temukan saat membuat website responsive adalah menyesuaikan layout yang awalnya dibuat untuk desktop agar tetap enak dilihat di mobile. Beberapa elemen yang berdampingan harus diubah menjadi kolom ke bawah, ukuran gambar perlu disesuaikan, dan jarak antar elemen juga perlu diperhatikan agar tidak terlalu sempit. Saya mengevaluasinya dengan mencoba tampilan web pada ukuran layar yang berbeda dan melihat elemen mana yang terlalu mepet/tidak enak dilihat. Dari situ saya menggunakan media untuk mengubah layout dan ukuran elemen yang perlu sedikit penyesuaian

3. Dalam proses pembuatan website ini, saya mulai memahami bahwa static web memiliki keterbatasan dalam menyediakan fitur yang membutuhkan interaksi dan perubahan data secara dinamis. Namun, setelah mencoba membuat website ini, saya mulai memiliki beberapa fitur yang ingin saya pelajari untuk iterasi selanjutnya, seperti dark mode dan light mode serta header yang dapat menyesuaikan saat pengguna melakukan scroll, misalnya header menghilang ketika scroll ke bawah dan muncul kembali ketika scroll sedikit ke atas


### Tugas 2

1. Misalnya pengguna saat ini berada di halaman Profile portofolio saya lalu click "Interest" di navigation bar, maka browser akan mengirim request GET ke alamat /interest/. Request ini pertama kali akan diterima oleh urls.py milik project (portofolio/urls.py). Dari situ request diterusin ke urls.py punya main lewat include("main.urls"). Di main/urls.py, interest/ udah didaftarin dan diarahin ke fungsi show_interest yang ada di views.py. Fungsi ini kemudian ngambil semua data Interest dari database lalu memisahkannya jadi dua group berdasarkan categorynya (exploring and fun). Data tersebut kemudian dikirim sebagai context ke template interest.html. Setelah itu, Django memproses template tersebut dengan data yang udah diambil dari database jadi HTML, dan hasil HTML yang sudah berisi data sesungguhnyalah yang akhirnya terlihat di browser pengguna

2. Data untuk bagian portofolio baru sebaiknya disimpan di model bukan langsung ditulis di template karena kalau datanya di-hardcode di HTML, setiap kali mau nambah atau mengubah data, saya harus edit file templatenya secara manual. Selain lebih ribet, cara tersebut juga lebih gampang bikin kesalahan kalau datanya udah banyak. Kalau datanya disimpen di model, saya bisa nambah, edit, atau menghapus datanya lewat Django Admin tanpa perlu ribet-ribet mengubah kode HTML. Hal ini juga membuat webnya lebih gampang buat di-maintain dan dikembangin di masa depan

3. makemigrations digunakan untuk membuat file migrasi yang mencatat perubahan yang terjadi di model, sedangkan migrate digunakan untuk menerapkan perubahan tersebut ke database. Contoh yang terjadi di saya yaitu salah satunya saat saya menghapus field category dari model Experience. Setelah field tersebut dihapus dari models.py, saya menjalankan makemigrations dan Django membuat file migrasi baru yang mencatat kalau field category dihapus. Tapi perubahan tersebut belum langsung terjadi di database. Setelah saya menjalankan migrate, barulah perubahan itu diterapkan ke db.sqlite3 dan kolom category ikut terhapus. Jadi, kalau cuman menjalankan makemigrations tanpa migrate, perubahan di database belum terjadi walau file migrasinya udah ada/dibuat.

Saya juga menggunakan bantuan gen AI dalam proses pengerjaan tugas, terutama untuk memahami HTML dan CSS, mencari solusi ketika mengalami kendala, dan referensi layout. Berikut tautan chatnya: https://share.gemini.google/fiaOIzhnKOir


Selain itu, saya juga menggunakan beberapa sumber maupun inspirasi lainnya yang saya cantumkan pada tautan berikut:

https://mimo.org/glossary/html/line-breaks

https://www.geeksforgeeks.org/html/how-to-add-horizontal-line-in-html/

https://w3schools.dev/css/default.asp

https://bahasaweb.com/tutorial-css-position-lengkap-static-relative-absolute-fixed-dan-sticky/

https://youtu.be/aswRKAjjWuE?si=6PdiwT4tnSbLBvUQ

https://freefrontend.com/css-hover-effects/

https://youtu.be/z2LQYsZhsFw?si=sDsAaFl1dpBWNP4l

https://youtu.be/hX35lQzTjK0?si=mzBR3Xc3JD1RbFZl

https://youtu.be/Inh6WKfzxV8?si=IlE1zeP-W52YOc9-

https://stackoverflow.com/questions/29980211/whats-the-difference-between-migrate-and-makemigrations-in-django