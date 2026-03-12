#!/usr/bin/env python3
"""
Laravel Deploy Packager - GUI Version
Context menu integration for right-click deployment packaging
"""

import os
import zipfile
import shutil
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
        
        # Setup patterns (sama seperti sebelumnya)
        self.include_patterns = [
            'app/**',
            'bootstrap/app.php',
            'bootstrap/providers.php',
            'config/**',
            'database/**',
            'lang/**',
            'resources/**',
            'routes/**',
            'public/build/**',
            'public/css/**',
            'public/js/**',
            'public/fonts/**',
            'public/images/**',
            'public/favicon.ico',
            'public/index.php',
            'public/robots.txt',
            'storage/app/public/.gitignore',
            'storage/framework/.gitignore',
            'storage/logs/.gitignore',
            'composer.json',
            'composer.lock',
            'package-lock.json',
            'artisan',
            'server.php',
            '.env.example',
        ]
        
        self.exclude_patterns = [
            'node_modules/**',
            'vendor/**',
            'resources/css/**',
            'resources/js/**',
            'resources/sass/**',
            'resources/less/**',
            'resources/ts/**',
            'resources/assets/**',
            'bootstrap/cache/*.php',
            'storage/framework/cache/**',
            'storage/framework/sessions/**',
            'storage/framework/views/**',
            'storage/framework/testing/**',
            'storage/logs/*.log',
            'storage/debugbar/**',
            '.git/**',
            '.gitignore',
            '.gitattributes',
            '.github/**',
            '.idea/**',
            '.vscode/**',
            '*.sublime-project',
            '*.sublime-workspace',
            '.editorconfig',
            'tests/**',
            'phpunit.xml',
            'phpunit.xml.dist',
            '.phpunit.result.cache',
            'coverage/**',
            '.env',
            '.env.*',
            'docker-compose*.yml',
            'docker-compose*.yaml',
            'Dockerfile*',
            '.dockerignore',
            'docker/**',
            'vite.config.js',
            'vite.config.ts',
            'webpack.mix.js',
            'webpack.config.js',
            'tailwind.config.js',
            'postcss.config.js',
            'babel.config.js',
            'tsconfig.json',
            'jsconfig.json',
            '.travis.yml',
            '.gitlab-ci.yml',
            '.styleci.yml',
            'README.md',
            'readme.md',
            'CHANGELOG.md',
            'changelog.md',
            'CONTRIBUTING.md',
            'LICENSE',
            'LICENSE.md',
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
        ]
        
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title(f"Laravel Deploy Packager - {self.folder_name}")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        self.style.configure('Info.TLabel', font=('Segoe UI', 10))
        
        # Header
        header = ttk.Frame(self.root, padding="20")
        header.pack(fill='x')
        
        ttk.Label(header, text="🚀 Laravel Deploy Packager", 
                 style='Title.TLabel').pack(anchor='w')
        ttk.Label(header, text=f"Target: {self.target_folder}", 
                 style='Info.TLabel').pack(anchor='w', pady=(5,0))
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20)
        
        # Main Content
        content = ttk.Frame(self.root, padding="20")
        content.pack(fill='both', expand=True)
        
        # Info Frame
        info_frame = ttk.LabelFrame(content, text="Informasi Package", padding="10")
        info_frame.pack(fill='x', pady=(0,10))
        
        self.lbl_output = ttk.Label(info_frame, text=f"Output: {self.output_name}")
        self.lbl_output.pack(anchor='w')
        
        self.lbl_status = ttk.Label(info_frame, text="Status: Menunggu...", 
                                   foreground='gray')
        self.lbl_status.pack(anchor='w', pady=(5,0))
        
        # Progress
        self.progress = ttk.Progressbar(content, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        
        # Buttons Frame
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill='x', pady=20)
        
        self.btn_preview = ttk.Button(btn_frame, text="📋 Preview File", 
                                     command=self.run_preview, width=20)
        self.btn_preview.pack(side='left', padx=5)
        
        self.btn_create = ttk.Button(btn_frame, text="📦 Create ZIP", 
                                    command=self.run_create_zip, width=20)
        self.btn_create.pack(side='left', padx=5)
        
        self.btn_open = ttk.Button(btn_frame, text="📂 Open Folder", 
                                  command=self.open_folder, width=20, state='disabled')
        self.btn_open.pack(side='left', padx=5)
        
        # Log Area
        log_frame = ttk.LabelFrame(content, text="Log", padding="5")
        log_frame.pack(fill='both', expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, 
                                                 font=('Consolas', 9))
        self.log_area.pack(fill='both', expand=True)
        
        # Footer
        footer = ttk.Frame(self.root, padding="10")
        footer.pack(fill='x', side='bottom')
        
        ttk.Button(footer, text="Tutup", command=self.root.quit).pack(side='right')
        
        self.log(f"Ready. Target folder: {self.target_folder}")
    
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
        
        for pattern in self.exclude_patterns:
            if self.match_pattern(rel_path, pattern):
                return False
        
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
            
            dirs[:] = [d for d in dirs if self.should_include(
                str(relative_root / d) if str(relative_root) != '.' else d)]
            
            for file in files:
                file_path = root_path / file
                rel_path = file_path.relative_to(self.target_folder)
                rel_path_str = str(rel_path).replace('\\', '/')
                
                if self.should_include(rel_path_str):
                    files_to_zip.append((file_path, rel_path_str))
                else:
                    excluded_count += 1
        
        return files_to_zip, excluded_count
    
    def run_preview(self):
        self.btn_preview.config(state='disabled')
        self.set_status("Scanning files...", "blue")
        self.progress.start()
        
        def preview_task():
            try:
                files, excluded = self.scan_files()
                
                self.log(f"SCAN RESULT:")
                self.log(f"Included: {len(files)} files")
                self.log(f"Excluded: {excluded} files")
                self.log("-" * 50)
                
                # Show sample
                self.log("Sample included files:")
                for f in sorted([f[1] for f in files])[:15]:
                    self.log(f"  + {f}")
                if len(files) > 15:
                    self.log(f"  ... and {len(files)-15} more")
                
                self.set_status(f"Preview selesai. {len(files)} files akan di-include", "green")
                
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
                with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for idx, (file_path, arcname) in enumerate(files_to_zip, 1):
                        if idx % 50 == 0:
                            percent = (idx / len(files_to_zip)) * 100
                            self.set_status(f"Processing... {percent:.0f}%", "blue")
                            self.root.update()
                        
                        try:
                            size = file_path.stat().st_size
                            zipf.write(file_path, arcname)
                            total_size += size
                        except Exception as e:
                            self.log(f"Warning: Skip {arcname} - {e}")
                
                zip_size = self.output_path.stat().st_size
                compression = (1 - zip_size/total_size)*100 if total_size > 0 else 0
                
                self.log("-" * 50)
                self.log("ZIP CREATED SUCCESSFULLY!")
                self.log(f"File: {self.output_name}")
                self.log(f"Location: {self.output_path}")
                self.log(f"Original size: {self.format_size(total_size)}")
                self.log(f"ZIP size: {self.format_size(zip_size)}")
                self.log(f"Compression: {compression:.1f}%")
                
                self.set_status("ZIP berhasil dibuat!", "green")
                self.btn_open.config(state='normal')
                
                messagebox.showinfo("Sukses", 
                    f"Package berhasil dibuat!\n\nFile: {self.output_name}\n"
                    f"Size: {self.format_size(zip_size)}\n\n"
                    f"Lokasi: {self.output_path.parent}")
                
            except Exception as e:
                self.log(f"ERROR: {str(e)}")
                self.set_status("Gagal membuat ZIP!", "red")
                messagebox.showerror("Error", f"Gagal membuat ZIP:\n{str(e)}")
            finally:
                self.progress.stop()
                self.btn_create.config(state='normal')
                self.btn_preview.config(state='normal')
        
        threading.Thread(target=create_task, daemon=True).start()
    
    def open_folder(self):
        os.startfile(self.output_path.parent)
    
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
        # Jika dijalankan tanpa argumen, buka file dialog
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