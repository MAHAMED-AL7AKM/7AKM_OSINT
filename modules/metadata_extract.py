import os
from PIL import Image
from PIL.ExifTags import TAGS
import PyPDF2
from mutagen import File as MutagenFile
from colorama import Fore, Style
from prettytable import PrettyTable

def search(filepath):
    print(Fore.YELLOW + f"[*] Extracting metadata from: {filepath}" + Style.RESET_ALL)
    if not os.path.exists(filepath):
        print(Fore.RED + "[!] File not found.")
        return None

    ext = os.path.splitext(filepath)[1].lower()
    result = {"file": filepath, "metadata": {}}

    try:
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            image = Image.open(filepath)
            exifdata = image.getexif()
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                result["metadata"][tag] = str(value)
            print(Fore.GREEN + "[+] Image metadata extracted.")
        elif ext == '.pdf':
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata
                if info:
                    for key, val in info.items():
                        result["metadata"][key] = str(val)
            print(Fore.GREEN + "[+] PDF metadata extracted.")
        elif ext in ['.mp3', '.flac', '.ogg', '.m4a']:
            audio = MutagenFile(filepath)
            if audio:
                for key, val in audio.items():
                    result["metadata"][key] = str(val)
            print(Fore.GREEN + "[+] Audio metadata extracted.")
        else:
            print(Fore.YELLOW + "[-] Unsupported file type.")
            return None

        if result["metadata"]:
            table = PrettyTable()
            table.field_names = ["Tag", "Value"]
            for k, v in result["metadata"].items():
                if len(str(v)) > 50:
                    v = str(v)[:50] + "..."
                table.add_row([k, v])
            print(table)
        else:
            print(Fore.YELLOW + "[-] No metadata found.")
        return result
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None