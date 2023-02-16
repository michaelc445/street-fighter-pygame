pyinstaller --hidden-import game -F --paths=/home/michael/PycharmProjects/pygame-client/venv/lib/python3.10/site-packages main.py
chmod +x dist/main
./dist/main