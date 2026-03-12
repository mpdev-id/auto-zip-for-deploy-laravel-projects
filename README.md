<h2>Installasi</h2>

<p>Ada dua cara untuk menginstall Laravel Deploy Packager:</p>

<h3>Opsi A: Install Manual</h3>

<ul>
    <li>Buat folder <code>C:\Tools\</code></li>
    <li>Copy <code>laravel_deploy.py</code> dan <code>laravel_deploy.bat</code> ke <code>C:\Tools\</code></li>
    <li>Edit <code>laravel_deploy.bat</code> - pastikan path <code>SCRIPT_PATH</code> benar</li>
    <li>Double-click <code>add_context_menu.reg</code> (edit dulu pathnya sesuai lokasi Anda)</li>
</ul>

<h3>Opsi B: Install dengan PowerShell (Recommended)</h3>

<ul>
    <li>Simpan semua file dalam satu folder</li>
    <li>Klik kanan <code>install.ps1</code> → Run with PowerShell (as Admin)</li>
    <li>Selesai!</li>
</ul>

<h2>Cara Pakai</h2>

<p>Klik kanan folder Laravel project Anda</p>

<p>Pilih " Deploy Laravel Project"</p>

<p>GUI akan muncul dengan 2 pilihan:</p>

<ul>
    <li>Preview File: Lihat daftar file yang akan di-include</li>
    <li>Create ZIP: Buat file ZIP dengan nama <code>namaFolder_deploy_TIMESTAMP.zip</code></li>
</ul>

<h3>Fitur GUI</h3>

<ul>
    <li>Progress bar saat membuat ZIP</li>
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

<a name="install"></a>
<h2>Install Laravel Deploy Packager</h2>

<p>Click the green <code>Code</code> button above and download the repository as a ZIP file.</p>

<p>Extract the contents of the ZIP file to a folder in your computer.</p>

<p>Open the folder in your terminal and run the command:</p>

<pre>
composer install --no-dev --optimize-autoloader
</pre>

<p>Follow the instructions in the <code>install.ps1</code> file to finish the installation.</p>

<h2>Setup Environment</h2>

<p>Edit the <code>.env</code> file to configure your database and other settings.</p>

<h2>Laravel Setup</h2>

<p>Run the following commands to setup Laravel:</p>

<pre>
php artisan key:generate
php artisan migrate --force
php artisan optimize
php artisan storage:link
</pre>

<h2>Permissions</h2>

<p>Run the following command to set permissions:</p>

<pre>
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data .
</pre>
