"""
Network Tester - Build Script
Creates a portable system tray application with bytecode protection
"""
import py_compile
import shutil
import zipapp
from pathlib import Path
import compileall
import os


def clean_build_dir(build_dir):
    """Remove build directory if it exists."""
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()


def compile_python_files(source_dir, build_dir):
    """Compile Python source files to bytecode."""
    print(f"Compiling {source_dir}...")
    
    compileall.compile_dir(
        source_dir,
        force=True,
        quiet=1,
        optimize=2
    )
    
    for root, dirs, files in os.walk(source_dir):
        rel_path = Path(root).relative_to(source_dir)
        
        for file in files:
            if file.endswith('.py'):
                source_file = Path(root) / file
                pycache_dir = Path(root) / '__pycache__'
                
                if pycache_dir.exists():
                    for pyc_file in pycache_dir.glob(f'{file[:-3]}.*.pyc'):
                        target_dir = build_dir / rel_path
                        target_dir.mkdir(parents=True, exist_ok=True)
                        
                        target_file = target_dir / (file + 'c')
                        shutil.copy2(pyc_file, target_file)
                        print(f"  ✓ Compiled: {rel_path / file}")


def copy_non_python_files(source_dir, build_dir, pattern='*.json'):
    """Copy configuration and other non-Python files."""
    for file in Path(source_dir).glob(pattern):
        target = build_dir / file.name
        shutil.copy2(file, target)
        print(f"  ✓ Copied: {file.name}")


def create_main_file(build_dir):
    """Create a minimal __main__.py that imports the compiled code."""
    main_content = '''"""Network Tester GUI - Compiled Version"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main_gui import main

if __name__ == "__main__":
    main()
'''
    
    main_file = build_dir / '__main__.py'
    main_file.write_text(main_content)
    print("  ✓ Created __main__.py")


def build_compiled_gui():
    """Main build function for GUI version."""
    print("=" * 60)
    print("Building Compiled Network Tester GUI")
    print("Source code will be protected (bytecode only)")
    print("=" * 60)
    print()
    
    build_dir = Path('build_compiled_gui')
    
    print("[1/6] Cleaning build directory...")
    clean_build_dir(build_dir)
    print()
    
    print("[2/6] Compiling services...")
    compile_python_files(Path('services'), build_dir / 'services')
    print()
    
    print("[3/6] Compiling src...")
    compile_python_files(Path('src'), build_dir / 'src')
    print()
    
    print("[4/6] Compiling main_gui.py...")
    compileall.compile_file('main_gui.py', force=True, quiet=1, optimize=2)
    
    pycache = Path('__pycache__')
    for pyc_file in pycache.glob('main_gui.*.pyc'):
        shutil.copy2(pyc_file, build_dir / 'main_gui.pyc')
        print("  ✓ Compiled: main_gui.py")
    print()
    
    print("[5/6] Copying configuration...")
    copy_non_python_files(Path('.'), build_dir, '*.json')
    print()
    
    print("[6/6] Creating entry point...")
    create_main_file(build_dir)
    print()
    
    print("[7/7] Packaging into single file...")
    output_file = Path('NetworkTester_GUI.pyz')
    
    # For Windows GUI mode, we don't set a shebang since .pyz files
    # need to be run with pythonw explicitly to hide the console
    zipapp.create_archive(
        build_dir,
        output_file,
        interpreter=None,  # No shebang - run with pythonw manually
        compressed=True
    )
    
    shutil.rmtree(build_dir)
    
    if output_file.exists():
        size_kb = output_file.stat().st_size / 1024
        print()
        print("=" * 60)
        print("✓ Build Successful!")
        print("=" * 60)
        print()
        print(f"Created: {output_file}")
        print(f"Size: {size_kb:.2f} KB")
        print()
        print("🔒 Source code protected (bytecode compilation)")
        print("🌐 Portable system tray application")
        print("⚡ Real-time settings reload")
        print("📊 Live statistics windows")
        print()
        print("To run: Double-click NetworkTester_GUI.vbs")
        print("Or run: pythonw NetworkTester_GUI.pyz")
        print()
    else:
        print("✗ Build failed!")
        return False
    
    return True


if __name__ == '__main__':
    try:
        success = build_compiled_gui()
        if not success:
            input("\nPress Enter to exit...")
            exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        exit(1)
    
    input("\nPress Enter to exit...")
