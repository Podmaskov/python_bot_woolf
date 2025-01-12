import json
import re
from datetime import datetime, timedelta
from models import Contact

class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.contacts = []
        self.filename = filename
        self.load_contacts()

    def add_contact(self, contact):
        """
        Додає новий контакт до книги контактів 
        після валідації телефону та email
        """
        if self.validate_phone(contact.phone) and self.validate_email(contact.email):
            self.contacts.append(contact)
            self.save_contacts()
            return True
        return False

    @staticmethod
    def validate_phone(self, phone):
        """ Валідує формат номера телефону за допомогою регулярного виразу"""
        pattern = re.compile(r'^\+?\d{10,15}$')
        return bool(pattern.match(phone))

    @staticmethod
    def validate_email(self, email):
        """ Валідує формат email за допомогою регулярного виразу"""
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(pattern.match(email))
    
    def save_contacts(self):
        """ Зберігає контакт у файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, ensure_ascii=False, indent=4)

    def load_contacts(self):
        """Завантажує контакти з файлу"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.contacts = [Contact.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []

    def upcoming_birthdays(self, days):
        """Отримує контакти з днями народження протягом заданої кількості днів"""
        upcoming = []
        today = datetime.today()
        target_date = today + timedelta(days=days)
        for contact in self.contacts:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= target_date:
                upcoming.append(contact)
        return upcoming

    def search_contacts(self, name):
        """ Шукає контакти за іменем"""
        return [contact for contact in self.contacts if name.lower() in contact.name.lower()]


    def edit_contact(self, name, **kwargs):
        """Редагує інформацію існуючого контакту"""
        for contact in self.contacts:
            if contact.name == name:
                for key, value in kwargs.items():
                    if hasattr(contact, key):
                        setattr(contact, key, value)
                self.save_contacts()
                return True
        return False
    def delete_contact(self, name):
        """Видаляє контакт з книги контактів"""
        for contact in self.contacts:
            if contact.name == name:
                self.contacts.remove(contact)
                self.save_contacts()
                 
                return True, "Контакт успішно видалено."
        return False, "Контакт не знайдено."