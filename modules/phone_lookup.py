import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import Fore, Style
from prettytable import PrettyTable

def search(phone):
    print(Fore.YELLOW + f"[*] Analyzing phone number: {phone}" + Style.RESET_ALL)
    try:
        parsed = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "[!] Invalid phone number.")
            return None
        
        table = PrettyTable()
        table.field_names = ["Field", "Value"]
        table.add_row(["International", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)])
        table.add_row(["National", phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)])
        table.add_row(["Country", geocoder.description_for_number(parsed, "en")])
        table.add_row(["Carrier", carrier.name_for_number(parsed, "en")])
        table.add_row(["Timezone", ', '.join(timezone.time_zones_for_number(parsed))])
        print(table)
        
        return {
            "phone": phone,
            "valid": True,
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "timezone": timezone.time_zones_for_number(parsed)
        }
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None