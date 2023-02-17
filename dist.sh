pyinstaller --hidden-import game -F --paths=`pwd`/venv/lib/python3.10/site-packages main.py
chmod +x dist/main
./dist/main