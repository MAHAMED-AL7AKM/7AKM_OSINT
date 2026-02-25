import os
import json
import requests
from faker import Faker
from PIL import Image, ImageDraw
from colorama import Fore, Style
from config import IDENTITIES_DIR
from utils.helpers import timestamp

fake = Faker()

def generate_face_image(save_path):
    url = "https://thispersondoesnotexist.com/image"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except:
        return False
    return False

def generate_id_card(identity, face_path, output_path):
    try:
        card = Image.new('RGB', (400, 250), color='white')
        draw = ImageDraw.Draw(card)
        draw.text((10, 10), f"Name: {identity['name']}", fill='black')
        draw.text((10, 30), f"DOB: {identity['birthdate']}", fill='black')
        draw.text((10, 50), f"Address: {identity['address'][:30]}", fill='black')
        draw.text((10, 70), f"Email: {identity['email']}", fill='black')
        draw.text((10, 90), f"Phone: {identity['phone']}", fill='black')
        if os.path.exists(face_path):
            face = Image.open(face_path).resize((100, 100))
            card.paste(face, (280, 10))
        card.save(output_path)
        return True
    except:
        return False

def generate():
    print(Fore.YELLOW + "[*] Generating new fake identity..." + Style.RESET_ALL)
    identity_id = timestamp()
    identity_dir = os.path.join(IDENTITIES_DIR, identity_id)
    os.makedirs(identity_dir, exist_ok=True)

    identity = {
        "id": identity_id,
        "name": fake.name(),
        "address": fake.address().replace('\n', ', '),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "nationality": fake.country(),
        "job": fake.job(),
        "company": fake.company(),
        "username": fake.user_name(),
        "password": fake.password(),
        "credit_card": fake.credit_card_full()
    }

    with open(os.path.join(identity_dir, "identity.json"), 'w') as f:
        json.dump(identity, f, indent=4)

    face_path = os.path.join(identity_dir, "face.jpg")
    if generate_face_image(face_path):
        print(Fore.GREEN + "[+] Face image generated.")

    id_card_path = os.path.join(identity_dir, "id_card.jpg")
    if generate_id_card(identity, face_path, id_card_path):
        print(Fore.GREEN + "[+] ID card generated.")

    print(Fore.GREEN + f"\n[+] Identity generated successfully!")
    print(Fore.CYAN + f"ID: {identity_id}")
    print(Fore.CYAN + f"Name: {identity['name']}")
    print(Fore.CYAN + f"Email: {identity['email']}")
    print(Fore.CYAN + f"Phone: {identity['phone']}")
    print(Fore.CYAN + f"Saved in: {identity_dir}")
    return identity