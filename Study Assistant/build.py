#!/usr/bin/env python3
"""
Build Script for Study Assistant
Creates standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages for building"""
    print("📦 Installing build requirements...")
    requirements = [
        "pyinstaller",
        "pyqt6",
        "pillow",
        "requests"
    ]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ Installed: {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {req}")

def create_spec_file():
    """Create PyInstaller spec file with custom settings"""
    
    # Check what directories exist
    datas = []
    if os.path.exists('src'):
        datas.append(('src', 'src'))
    if os.path.exists('assets'):
        datas.append(('assets', 'assets'))
    if os.path.exists('resources'):
        datas.append(('resources', 'resources'))
    
    # Convert datas list to string format
    datas_str = str(datas).replace("'", '"')
    
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas={datas_str},
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'sqlite3',
        'PIL',
        'requests',
        'nltk',
        'sumy',
        'nltk.corpus',
        'nltk.tokenize',
        'nltk.stem',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'scipy',
        'scipy.spatial',
        'scipy.sparse',
        'scipy.linalg',
        'scipy.stats',
        'scipy.interpolate',
        'scipy.integrate',
        'scipy.optimize',
        'scipy.signal',
        'scipy.fftpack'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StudyAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    description='Study Assistant - Ứng dụng học tập thông minh',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    upx=True,
    upx_exclude=[],
    name='StudyAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('StudyAssistant.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ Created StudyAssistant.spec")

def build_app():
    """Build the application using PyInstaller"""
    print("🔨 Building Study Assistant...")
    
    try:
        # Create spec file
        create_spec_file()
        
        # Build using PyInstaller
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller', 
            '--clean', 
            '--noconfirm',
            'StudyAssistant.spec'
        ])
        
        print("✅ Build completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_installer():
    """Create installer using NSIS (optional)"""
    print("📦 Creating installer...")
    
    nsis_script = '''
!define APPNAME "Study Assistant"
!define VERSION "1.0.0"
!define PUBLISHER "Study Assistant Team"

Name "${APPNAME}"
OutFile "${APPNAME} Setup.exe"
InstallDir "$PROGRAMFILES\\${APPNAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File /r "dist\\StudyAssistant\\*"
    CreateShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\StudyAssistant.exe"
    CreateShortCut "$STARTMENU\\Programs\\${APPNAME}.lnk" "$INSTDIR\\StudyAssistant.exe"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\\${APPNAME}.lnk"
    Delete "$STARTMENU\\Programs\\${APPNAME}.lnk"
    RMDir /r "$INSTDIR"
SectionEnd
'''
    
    with open('installer.nsi', 'w', encoding='utf-8') as f:
        f.write(nsis_script)
    
    print("📝 Created installer.nsi")
    print("💡 To create installer, run: makensis installer.nsi")

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['StudyAssistant.spec', 'installer.nsi']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Removed: {dir_name}")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🗑️ Removed: {file_name}")

def main():
    """Main build process"""
    print("🚀 Study Assistant Build Script")
    print("=" * 50)
    
    # Change to main app directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # Install requirements
    install_requirements()
    
    # Build the app
    if build_app():
        print("\n🎉 Build completed!")
        print(f"📁 Output: dist/StudyAssistant/")
        
        # Create installer script
        create_installer()
        
        print("\n📋 Build Summary:")
        print("✅ Application built successfully!")
        print("📁 Location: dist/StudyAssistant/")
        print("📦 Installer script: installer.nsi")
        print("🔧 To clean: python build.py --clean")
        
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        clean_build()
    else:
        main()
