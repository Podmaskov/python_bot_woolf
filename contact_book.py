import json
import re
from datetime import datetime, timedelta
from models import Contact
from colorama import Fore, Style

class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.contacts = []
        self.filename = filename
        self.load_contacts()

    # Додає новий контакт до книги контактів після валідації телефону та email
    def add_contact(self, contact):
        if self.validate_phone(contact.phone) and self.validate_email(contact.email):
            self.contacts.append(contact)
            self.save_contacts()
            print(Fore.GREEN + "Контакт успішно додано.")
        else:
            print(Fore.RED + "Некоректний номер телефону або email.")

    # Валідує формат номера телефону за допомогою регулярного виразу
    def validate_phone(self, phone):
        pattern = re.compile(r'^\+?\d{10,15}$')
        return bool(pattern.match(phone))

    # Валідує формат email за допомогою регулярного виразу
    def validate_email(self, email):
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(pattern.match(email))
    
    # Зберігає контакт у файл
    def save_contacts(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, ensure_ascii=False, indent=4)

    # Завантажує контакти з файлу
    def load_contacts(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.contacts = [Contact.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []

    # Отримує контакти з днями народження протягом заданої кількості днів
    def upcoming_birthdays(self, days):
        upcoming = []
        today = datetime.today()
        target_date = today + timedelta(days=days)
        for contact in self.contacts:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= target_date:
                upcoming.append(contact)
        return upcoming

    # Шукає контакти за іменем
    def search_contacts(self, name):
        return [contact for contact in self.contacts if name.lower() in contact.name.lower()]

   # Редагує інформацію існуючого контакту
    def edit_contact(self, name, **kwargs):
        for contact in self.contacts:
            if contact.name == name:
                for key, value in kwargs.items():
                    if hasattr(contact, key):
                        setattr(contact, key, value)
                self.save_contacts()
                print(Fore.GREEN + "Контакт успішно оновлено.")
                return
        print(Fore.RED + "Контакт не знайдено.")

    # Видаляє контакт з книги контактів
    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                self.contacts.remove(contact)
                self.save_contacts()
                print(Fore.GREEN + "Контакт успішно видалено.")
                return
        print(Fore.RED + "Контакт не знайдено.")