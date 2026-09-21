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


### Tugas 3

1. Kita menggunakan ModelForm karena ModelForm dapat membuat form berdasarkan model Django yang sudah dibuat, jadi kita tidak perlu nulis semua field form secara manual dalam HTML. ModelForm juga membantu proses validasi dan penyimpanan data ke database jadi lebih mudah dan terstruktur. Sementara itu {% csrf_token %} digunakan untuk keamanan saat form mengirim data, terutama dengan method POST. Token ini membantu memastikan bahwa request yang masuk benar benar berasal dari form pada website kita, sehingga mencegah pihak lain mengirim request secara sembarangan melalui website lain.

2. JSON lebih sering digunakan dalam pengembangan web modern karena formatnya lebih sederhana dibandingkan XML. Bentuk penulisannya juga cukup mudah dibaca dan dipahami, karena menggunakan pasangan key dan value. Selain itu, JSON juga lebih mudah digunakan oleh berbagai bahasa pemrograman dan sangat umum dipakai untuk komunikasi antara frontend dan backend. Jadi, untuk aplikasi web yang perlu sering bertukar data, JSON biasanya lebih praktis daripada XML

3. Ketika kita mengakses URL untuk melihat data portofolio dalam bentuk JSON, request dari pengguna akan diteruskan dari urls.py ke fungsi view yang sesuai. Di dalam view tersebut, kita mengambil data portofolio dari database menggunakan model Django. Masalahnya, data yang diambil dari database masih berbentuk object atau queryset Django, sehingga belum bisa langsung dikembalikan sebagai JSON. Karena itu, kita melakukan serialization, yaitu mengubah data tersebut ke bentuk yang lebih umum seperti dictionary atau list yang bisa direpresentasikan dalam JSON. Setelah proses tersebut selesai, data yang sudah berbentuk teks JSON dikembalikan melalui HttpResponse dengan content_type diatur ke application/json, sehingga data portofolio bisa ditampilkan dalam format JSON dan juga dapat dibaca oleh aplikasi atau frontend lain
---------------------------------------------------------------------------------------

Saya juga menggunakan bantuan gen AI dalam proses pengerjaan tugas, terutama untuk memahami tugas dan mencari solusi ketika mengalami kendala. Berikut tautan chatnya: https://share.gemini.google/I7AsKpGsWLnz (akan selalu menggunakan room chat yang sama)


Selain itu, saya juga menggunakan beberapa sumber maupun inspirasi lainnya yang saya cantumkan pada tautan berikut:

* https://mimo.org/glossary/html/line-breaks

* https://www.geeksforgeeks.org/html/how-to-add-horizontal-line-in-html/

* https://w3schools.dev/css/default.asp

* https://bahasaweb.com/tutorial-css-position-lengkap-static-relative-absolute-fixed-dan-sticky/

* https://youtu.be/aswRKAjjWuE?si=6PdiwT4tnSbLBvUQ

* https://freefrontend.com/css-hover-effects/

* https://youtu.be/z2LQYsZhsFw?si=sDsAaFl1dpBWNP4l

* https://youtu.be/hX35lQzTjK0?si=mzBR3Xc3JD1RbFZl

* https://youtu.be/Inh6WKfzxV8?si=IlE1zeP-W52YOc9-

* https://stackoverflow.com/questions/29980211/whats-the-difference-between-migrate-and-makemigrations-in-django

* https://youtu.be/I2-JYxnSiB0?si=uJRuREe1FSuhq_eN