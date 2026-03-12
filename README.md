<h2>Cara Install:</h2>

<p>Opsi A: Install Manual</p>
<ul>
    <li>Buat folder C:\Tools\</li>
    <li>Copy laravel_deploy.py dan laravel_deploy.bat ke C:\Tools\</li>
    <li>Edit laravel_deploy.bat - pastikan path SCRIPT_PATH benar</li>
    <li>Double-click add_context_menu.reg (edit dulu pathnya sesuai lokasi Anda)</li>
</ul>

<p>Opsi B: Install dengan PowerShell (Recommended)</p>
<ul>
    <li>Simpan semua file dalam satu folder</li>
    <li>Klik kanan install.ps1 → Run with PowerShell (as Admin)</li>
    <li>Selesai!</li>
</ul>

<h2>Cara Pakai:</h2>

<p>Klik kanan folder Laravel project Anda</p>
<p>Pilih " Deploy Laravel Project"</p>
<p>GUI akan muncul dengan 2 pilihan:</p>
<ul>
    <li> Preview File: Lihat daftar file yang akan di-include</li>
    <li>Create ZIP: Buat file ZIP dengan nama namaFolder_deploy_TIMESTAMP.zip</li>
</ul>

<h3>Fitur GUI:</h3>

<ul>
    <li> Progress bar saat membuat ZIP</li>
    <li>Log realtime menunjukkan proses</li>
    <li>Preview file yang akan di-include</li>
    <li>Open Folder setelah ZIP selesai dibuat</li>
    <li>Compression info (berapa % space yang dihemat)</li>
    <li>Threading (GUI tidak freeze saat proses)</li>
</ul>

<p>Hasil ZIP akan disimpan di folder parent dari target folder (satu level di atas project).</p>
<p>Contoh:</p>
<pre>
Project: D:\Projects\MyLaravelApp\
Output: D:\Projects\MyLaravelApp_deploy_20240312_143022.zip
</pre>

<p>Silakan dicoba! Jika ada error atau perlu modifikasi pattern file, bisa disesuaikan di bagian include_patterns dan exclude_patterns di script Python.</p>
