"""
Build script to create a compiled, obfuscated portable application
Compiles Python to bytecode (.pyc) so source code cannot be easily read
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
    """
    Compile Python source files to bytecode.
    This removes the source code visibility.
    """
    print(f"Compiling {source_dir}...")
    
    # Compile all Python files to .pyc
    compileall.compile_dir(
        source_dir,
        force=True,
        quiet=1,
        optimize=2  # Optimize level 2: removes docstrings and assertions
    )
    
    # Copy only .pyc files (compiled bytecode)
    for root, dirs, files in os.walk(source_dir):
        # Skip __pycache__ in source
        rel_path = Path(root).relative_to(source_dir)
        
        for file in files:
            if file.endswith('.py'):
                # Find corresponding .pyc file
                source_file = Path(root) / file
                pycache_dir = Path(root) / '__pycache__'
                
                if pycache_dir.exists():
                    # Look for compiled .pyc files
                    for pyc_file in pycache_dir.glob(f'{file[:-3]}.*.pyc'):
                        # Create target directory
                        target_dir = build_dir / rel_path
                        target_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Copy .pyc with original name
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
    main_content = '''"""Network Tester - Compiled Version"""
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the main function from compiled code
from main import main

if __name__ == "__main__":
    main()
'''
    
    main_file = build_dir / '__main__.py'
    main_file.write_text(main_content)
    print("  ✓ Created __main__.py")


def build_compiled_app():
    """Main build function."""
    print("=" * 60)
    print("Building Compiled Network Tester")
    print("Source code will be protected (bytecode only)")
    print("=" * 60)
    print()
    
    build_dir = Path('build_compiled')
    
    # Step 1: Clean build directory
    print("[1/6] Cleaning build directory...")
    clean_build_dir(build_dir)
    print()
    
    # Step 2: Compile services directory
    print("[2/6] Compiling services...")
    compile_python_files(Path('services'), build_dir / 'services')
    print()
    
    # Step 3: Compile src directory
    print("[3/6] Compiling src...")
    compile_python_files(Path('src'), build_dir / 'src')
    print()
    
    # Step 4: Compile main.py
    print("[4/6] Compiling main.py...")
    compileall.compile_file('main.py', force=True, quiet=1, optimize=2)
    
    # Copy the compiled main.pyc
    pycache = Path('__pycache__')
    for pyc_file in pycache.glob('main.*.pyc'):
        shutil.copy2(pyc_file, build_dir / 'main.pyc')
        print("  ✓ Compiled: main.py")
    print()
    
    # Step 5: Copy config file
    print("[5/6] Copying configuration...")
    copy_non_python_files(Path('.'), build_dir, '*.json')
    print()
    
    # Step 6: Create __main__.py
    print("[6/6] Creating entry point...")
    create_main_file(build_dir)
    print()
    
    # Step 7: Create zipapp
    print("[7/7] Packaging into single file...")
    output_file = Path('NetworkTester_Compiled.pyz')
    
    zipapp.create_archive(
        build_dir,
        output_file,
        interpreter='/usr/bin/env python',
        compressed=True
    )
    
    # Cleanup
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
        print("Source code is now compiled to bytecode (.pyc)")
        print("Users cannot easily read your code!")
        print()
        print("To run: python NetworkTester_Compiled.pyz")
        print()
    else:
        print("✗ Build failed!")
        return False
    
    return True


if __name__ == '__main__':
    try:
        success = build_compiled_app()
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
