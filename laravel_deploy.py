#!/usr/bin/env python3
"""
Laravel Deploy Packager - GUI Version
Fixed: Ensure all essential files are included
"""

import os
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
import fnmatch
import sys
import threading

class LaravelDeployGUI:
    def __init__(self, target_folder):
        self.target_folder = Path(target_folder).resolve()
        self.folder_name = self.target_folder.name
        self.output_name = f"{self.folder_name}_deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        self.output_path = self.target_folder.parent / self.output_name
        
        # CRITICAL: Explicitly list all required files
        self.critical_files = [
            # Middleware (WAJIB ADA)
            'app/Http/Middleware/EncryptCookies.php',
            'app/Http/Middleware/VerifyCsrfToken.php',
            'app/Http/Middleware/TrimStrings.php',
            'app/Http/Middleware/RedirectIfAuthenticated.php',
            'app/Http/Middleware/Authenticate.php',
            
            # Kernel
            'app/Http/Kernel.php',
            'app/Console/Kernel.php',
            
            # Providers
            'app/Providers/AppServiceProvider.php',
            'app/Providers/AuthServiceProvider.php',
            'app/Providers/EventServiceProvider.php',
            'app/Providers/RouteServiceProvider.php',
            
            # Exceptions
            'app/Exceptions/Handler.php',
            
            # Models
            'app/Models/User.php',
            
            # Bootstrap
            'bootstrap/app.php',
            'bootstrap/providers.php',
        ]
        
        # Include patterns - PASTIKAN app/** mencakup semua
        self.include_patterns = [
            'app/**',           # SEMUA file di app
            'bootstrap/**',     # SEMUA file di bootstrap
            'config/**',        # SEMUA config
            'database/**',      # SEMUA database
            'lang/**',          # SEMUA lang
            'resources/**',     # SEMUA resources
            'routes/**',        # SEMUA routes
            'public/**',        # SEMUA public
            'storage/**',       # SEMUA storage structure
            
            # Root files
            'composer.json',
            'composer.lock',
            'package-lock.json',
            'artisan',
            'server.php',
            '.env.example',
            '.env',
        ]
        
        self.exclude_patterns = [
            # Dependencies
            'node_modules/**',
            'vendor/**',
            
            # Source assets (sudah di-build)
            'resources/css/**',
            'resources/js/**',
            'resources/sass/**',
            'resources/less/**',
            'resources/ts/**',
            'resources/assets/**',
            
            # Cache contents (exclude files, keep structure)
            'storage/framework/cache/data/*',
            'storage/framework/sessions/*',
            'storage/framework/views/*',
            'storage/framework/testing/*',
            'storage/logs/*.log',
            'storage/debugbar/**',
            'storage/*.key',
            
            # Version control
            '.git/**',
            '.gitignore',
            '.gitattributes',
            '.github/**',
            
            # IDE
            '.idea/**',
            '.vscode/**',
            '*.sublime-project',
            '*.sublime-workspace',
            '.editorconfig',
            
            # Testing
            'tests/**',
            'phpunit.xml',
            'phpunit.xml.dist',
            '.phpunit.result.cache',
            'coverage/**',
            
            # Dev environment
            '.env.local',
            '.env.development',
            '.env.testing',
            'docker-compose*.yml',
            'docker-compose*.yaml',
            'Dockerfile*',
            '.dockerignore',
            'docker/**',
            
            # Build configs
            'vite.config.js',
            'vite.config.ts',
            'webpack.mix.js',
            'webpack.config.js',
            'tailwind.config.js',
            'postcss.config.js',
            'babel.config.js',
            'tsconfig.json',
            'jsconfig.json',
            
            # CI/CD
            '.travis.yml',
            '.gitlab-ci.yml',
            '.styleci.yml',
            
            # Docs
            'README.md',
            'readme.md',
            'CHANGELOG.md',
            'changelog.md',
            'CONTRIBUTING.md',
            'LICENSE',
            'LICENSE.md',
            
            # Misc
            'Makefile',
            '*.sh',
            '*.bat',
            '*.log',
            '*.tmp',
            '*.temp',
            '.DS_Store',
            'Thumbs.db',
            '*.swp',
            '*.swo',
            '*~',
            '*.zip',
            'deploy_package.py',
            'laravel_deploy.py',
        ]
        
        # Required empty folders
        self.required_structure = {
            'bootstrap/cache': "*\n!.gitignore",
            'storage/framework/cache/data': "*\n!.gitignore",
            'storage/framework/sessions': "*\n!.gitignore",
            'storage/framework/views': "*\n!.gitignore",
            'storage/framework/testing': "*\n!.gitignore",
            'storage/logs': "*\n!.gitignore",
            'storage/app/public': "*\n!.gitignore",
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title(f"Laravel Deploy Packager - {self.folder_name}")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        self.style.configure('Info.TLabel', font=('Segoe UI', 10))
        self.style.configure('Critical.TLabel', font=('Segoe UI', 9), foreground='red')
        
        header = ttk.Frame(self.root, padding="20")
        header.pack(fill='x')
        
        ttk.Label(header, text="[LARAVEL DEPLOY PACKAGER]", 
                 style='Title.TLabel').pack(anchor='w')
        ttk.Label(header, text=f"Target: {self.target_folder}", 
                 style='Info.TLabel').pack(anchor='w', pady=(5,0))
        
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20)
        
        content = ttk.Frame(self.root, padding="20")
        content.pack(fill='both', expand=True)
        
        # Critical files frame
        critical_frame = ttk.LabelFrame(content, text="Critical Files Check", padding="10")
        critical_frame.pack(fill='x', pady=(0,10))
        
        self.lbl_critical = ttk.Label(critical_frame, text="Checking...", style='Critical.TLabel')
        self.lbl_critical.pack(anchor='w')
        
        # Info Frame
        info_frame = ttk.LabelFrame(content, text="Informasi Package", padding="10")
        info_frame.pack(fill='x', pady=(0,10))
        
        self.lbl_output = ttk.Label(info_frame, text=f"Output: {self.output_name}")
        self.lbl_output.pack(anchor='w')
        
        self.lbl_status = ttk.Label(info_frame, text="Status: Menunggu...", foreground='gray')
        self.lbl_status.pack(anchor='w', pady=(5,0))
        
        self.progress = ttk.Progressbar(content, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill='x', pady=20)
        
        self.btn_preview = ttk.Button(btn_frame, text="[ Preview File ]", 
                                     command=self.run_preview, width=20)
        self.btn_preview.pack(side='left', padx=5)
        
        self.btn_create = ttk.Button(btn_frame, text="[ Create ZIP ]", 
                                    command=self.run_create_zip, width=20)
        self.btn_create.pack(side='left', padx=5)
        
        self.btn_open = ttk.Button(btn_frame, text="[ Open Folder ]", 
                                  command=self.open_folder, width=20, state='disabled')
        self.btn_open.pack(side='left', padx=5)
        
        log_frame = ttk.LabelFrame(content, text="Log", padding="5")
        log_frame.pack(fill='both', expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=12, font=('Consolas', 9))
        self.log_area.pack(fill='both', expand=True)
        
        footer = ttk.Frame(self.root, padding="10")
        footer.pack(fill='x', side='bottom')
        
        ttk.Button(footer, text="Tutup", command=self.root.quit).pack(side='right')
        
        self.log(f"Ready. Target folder: {self.target_folder}")
        self.check_critical_files()
    
    def check_critical_files(self):
        """Check if critical files exist"""
        missing = []
        for file in self.critical_files:
            full_path = self.target_folder / file
            if not full_path.exists():
                missing.append(file)
        
        if missing:
            self.lbl_critical.config(text=f"WARNING: {len(missing)} critical files missing!")
            self.log("CRITICAL FILES MISSING:")
            for f in missing:
                self.log(f"  - {f}")
        else:
            self.lbl_critical.config(text="All critical files present", foreground='green')
            self.log("All critical files present")
    
    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_area.insert('end', f"[{timestamp}] {message}\n")
        self.log_area.see('end')
        self.root.update()
    
    def set_status(self, text, color='black'):
        self.lbl_status.config(text=f"Status: {text}", foreground=color)
    
    def match_pattern(self, path, pattern):
        path = path.replace('\\', '/')
        pattern = pattern.replace('\\', '/')
        
        if path == pattern:
            return True
        
        if pattern.endswith('/**'):
            dir_pattern = pattern[:-3]
            if path.startswith(dir_pattern + '/'):
                return True
            if path == dir_pattern:
                return True
        
        if pattern.startswith('**/'):
            file_pattern = pattern[3:]
            if fnmatch.fnmatch(path, file_pattern):
                return True
            if '/' in path:
                parts = path.split('/')
                for i in range(len(parts)):
                    sub_path = '/'.join(parts[i:])
                    if fnmatch.fnmatch(sub_path, file_pattern):
                        return True
        
        if fnmatch.fnmatch(path, pattern):
            return True
        
        if path.startswith(pattern + '/'):
            return True
            
        return False
    
    def should_include(self, relative_path):
        rel_path = relative_path.replace('\\', '/')
        
        # Check exclude patterns first
        for pattern in self.exclude_patterns:
            if self.match_pattern(rel_path, pattern):
                return False
        
        # Check include patterns
        for pattern in self.include_patterns:
            if self.match_pattern(rel_path, pattern):
                return True
        
        return False
    
    def scan_files(self):
        files_to_zip = []
        excluded_count = 0
        
        for root, dirs, files in os.walk(self.target_folder):
            root_path = Path(root)
            relative_root = root_path.relative_to(self.target_folder)
            
            filtered_dirs = []
            for d in dirs:
                rel_d = str(relative_root / d) if str(relative_root) != '.' else d
                if self.should_include(rel_d):
                    filtered_dirs.append(d)
            dirs[:] = filtered_dirs
            
            for file in files:
                file_path = root_path / file
                rel_path = file_path.relative_to(self.target_folder)
                rel_path_str = str(rel_path).replace('\\', '/')
                
                if self.should_include(rel_path_str):
                    files_to_zip.append((file_path, rel_path_str))
                else:
                    excluded_count += 1
        
        return files_to_zip, excluded_count
    
    def ensure_critical_files(self, zipf, files_to_zip):
        """Ensure all critical files are in the ZIP"""
        existing_files = {f[1] for f in files_to_zip}
        
        for critical_file in self.critical_files:
            if critical_file not in existing_files:
                full_path = self.target_folder / critical_file
                if full_path.exists():
                    self.log(f"  Adding critical file: {critical_file}")
                    zipf.write(full_path, critical_file)
                else:
                    self.log(f"  WARNING: Critical file missing: {critical_file}")
    
    def create_deployment_scripts(self, zipf):
        """Create helper scripts"""
        
        setup_script = '''#!/bin/bash
# Laravel Deployment Setup Script

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=== Laravel Deployment Setup ==="

WEB_USER="www-data"
if ps aux | grep -q "[n]ginx"; then
    WEB_USER="nginx"
elif ps aux | grep -q "[a]pache"; then
    WEB_USER="apache"
fi

echo "Detected web server user: $WEB_USER"

# Create storage structure
mkdir -p storage/framework/cache/data
mkdir -p storage/framework/sessions
mkdir -p storage/framework/views
mkdir -p storage/framework/testing
mkdir -p storage/logs
mkdir -p storage/app/public
mkdir -p bootstrap/cache

# Set permissions
chmod -R 777 storage bootstrap/cache
chown -R $WEB_USER:$WEB_USER storage bootstrap/cache 2>/dev/null || \
chown -R www-data:www-data storage bootstrap/cache 2>/dev/null || true

touch storage/logs/laravel.log
chmod 666 storage/logs/laravel.log

# Install dependencies
composer install --no-dev --optimize-autoloader

# Setup environment
if [ ! -f .env ]; then
    cp .env.example .env
    php artisan key:generate
fi

# Create storage symlink
rm -f public/storage
php artisan storage:link

# Optimize
php artisan optimize

echo "=== Setup Complete ==="
'''
        zipf.writestr("setup.sh", setup_script)
        
        # Create missing middleware script
        middleware_script = '''#!/bin/bash
# Create missing middleware files

mkdir -p app/Http/Middleware

cat > app/Http/Middleware/EncryptCookies.php << 'EOF'
<?php

namespace App\\Http\\Middleware;

use Illuminate\\Cookie\\Middleware\\EncryptCookies as Middleware;

class EncryptCookies extends Middleware
{
    protected $except = [];
}
EOF

cat > app/Http/Middleware/VerifyCsrfToken.php << 'EOF'
<?php

namespace App\\Http\\Middleware;

use Illuminate\\Foundation\\Http\\Middleware\\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    protected $except = [];
}
EOF

cat > app/Http/Middleware/TrimStrings.php << 'EOF'
<?php

namespace App\\Http\\Middleware;

use Illuminate\\Foundation\\Http\\Middleware\\TrimStrings as Middleware;

class TrimStrings extends Middleware
{
    protected $except = ['current_password', 'password', 'password_confirmation'];
}
EOF

echo "Middleware files created!"
'''
        zipf.writestr("create-middleware.sh", middleware_script)
        
        fix_script = '''#!/bin/bash
chmod -R 777 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache 2>/dev/null || true
touch storage/logs/laravel.log
chmod 666 storage/logs/laravel.log
php artisan cache:clear
php artisan view:clear
echo "Permissions fixed!"
'''
        zipf.writestr("fix-permissions.sh", fix_script)
        
        self.log("  Created: setup.sh")
        self.log("  Created: create-middleware.sh")
        self.log("  Created: fix-permissions.sh")
    
    def create_required_structure(self, zipf):
        """Create required folder structure"""
        self.log("Creating required folder structure...")
        
        for folder, gitignore_content in self.required_structure.items():
            zipf.writestr(f"{folder}/.gitkeep", "")
            zipf.writestr(f"{folder}/.gitignore", gitignore_content)
        
        self.create_deployment_scripts(zipf)
    
    def run_preview(self):
        self.btn_preview.config(state='disabled')
        self.set_status("Scanning files...", "blue")
        self.progress.start()
        
        def preview_task():
            try:
                files, excluded = self.scan_files()
                
                # Check critical files
                existing_files = {f[1] for f in files}
                missing_critical = [f for f in self.critical_files if f not in existing_files]
                
                self.log("=" * 50)
                self.log("SCAN RESULT")
                self.log("=" * 50)
                self.log(f"Files to include: {len(files)}")
                self.log(f"Files excluded: {excluded}")
                
                if missing_critical:
                    self.log(f"WARNING: {len(missing_critical)} critical files will be added separately")
                    for f in missing_critical:
                        self.log(f"  ! {f}")
                
                self.log("-" * 50)
                self.log("Sample included files:")
                for f in sorted([f[1] for f in files])[:15]:
                    self.log(f"  + {f}")
                
                self.set_status(f"Preview: {len(files)} files", "green")
                
            except Exception as e:
                self.log(f"ERROR: {str(e)}")
                self.set_status("Error!", "red")
            finally:
                self.progress.stop()
                self.btn_preview.config(state='normal')
        
        threading.Thread(target=preview_task, daemon=True).start()
    
    def run_create_zip(self):
        self.btn_create.config(state='disabled')
        self.btn_preview.config(state='disabled')
        self.set_status("Creating ZIP...", "blue")
        self.progress.start()
        
        def create_task():
            try:
                files_to_zip, excluded = self.scan_files()
                
                if not files_to_zip:
                    messagebox.showwarning("Warning", "Tidak ada file yang di-include!")
                    return
                
                total_size = 0
                file_count = 0
                
                with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Add scanned files
                    for idx, (file_path, arcname) in enumerate(files_to_zip, 1):
                        if idx % 50 == 0:
                            percent = (idx / len(files_to_zip)) * 100
                            self.set_status(f"Adding files... {percent:.0f}%", "blue")
                            self.root.update()
                        
                        try:
                            if file_path.exists():
                                size = file_path.stat().st_size
                                zipf.write(file_path, arcname)
                                total_size += size
                                file_count += 1
                        except Exception as e:
                            self.log(f"Warning: Skip {arcname} - {e}")
                    
                    # Ensure critical files are included
                    self.set_status("Checking critical files...", "blue")
                    self.ensure_critical_files(zipf, files_to_zip)
                    
                    # Create required structure
                    self.set_status("Creating folder structure...", "blue")
                    self.create_required_structure(zipf)
                
                zip_size = self.output_path.stat().st_size
                compression = (1 - zip_size/total_size)*100 if total_size > 0 else 0
                
                self.log("=" * 50)
                self.log("ZIP CREATED SUCCESSFULLY")
                self.log("=" * 50)
                self.log(f"File: {self.output_name}")
                self.log(f"Files added: {file_count}")
                self.log(f"ZIP size: {self.format_size(zip_size)}")
                
                self.set_status("ZIP created successfully!", "green")
                self.btn_open.config(state='normal')
                
                messagebox.showinfo("Sukses", 
                    f"Package berhasil dibuat!\n\n"
                    f"File: {self.output_name}\n"
                    f"Size: {self.format_size(zip_size)}\n\n"
                    f"Lokasi: {self.output_path.parent}")
                
            except Exception as e:
                self.log(f"ERROR: {str(e)}")
                import traceback
                self.log(traceback.format_exc())
                self.set_status("Failed to create ZIP!", "red")
                messagebox.showerror("Error", f"Gagal membuat ZIP:\n{str(e)}")
            finally:
                self.progress.stop()
                self.btn_create.config(state='normal')
                self.btn_preview.config(state='normal')
        
        threading.Thread(target=create_task, daemon=True).start()
    
    def open_folder(self):
        try:
            os.startfile(self.output_path.parent)
        except:
            import subprocess
            subprocess.Popen(['explorer', str(self.output_path.parent)])
    
    def format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def run(self):
        self.root.mainloop()

def main():
    if len(sys.argv) < 2:
        root = tk.Tk()
        root.withdraw()
        from tkinter import filedialog
        folder = filedialog.askdirectory(title="Pilih Folder Laravel Project")
        if not folder:
            return
        root.destroy()
    else:
        folder = sys.argv[1]
    
    if not Path(folder).exists():
        messagebox.showerror("Error", f"Folder tidak ditemukan:\n{folder}")
        return
    
    app = LaravelDeployGUI(folder)
    app.run()

if __name__ == "__main__":
    main()