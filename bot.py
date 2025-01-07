from dataclasses import dataclass, field
import re
from datetime import datetime, timedelta

@dataclass
class Contact:
    name: str
    address: str
    phone: str
    email: str
    birthday: datetime

@dataclass
class Note:
    content: str
    tags: list = field(default_factory=list)

class ContactBook:
    def __init__(self):
        self.contacts = []

    # Додає новий контакт до книги контактів після валідації телефону та email
    def add_contact(self, contact):
        if self.validate_phone(contact.phone) and self.validate_email(contact.email):
            self.contacts.append(contact)
            print("Контакт успішно додано.")
        else:
            print("Некоректний номер телефону або email.")

    # Валідує формат номера телефону за допомогою регулярного виразу
    def validate_phone(self, phone):
        pattern = re.compile(r'^\+?\d{10,15}$')
        return bool(pattern.match(phone))

    # Валідує формат email за допомогою регулярного виразу
    def validate_email(self, email):
        pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        return bool(pattern.match(email))

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
                print("Контакт успішно оновлено.")
                return
        print("Контакт не знайдено.")

    # Видаляє контакт з книги контактів
    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                self.contacts.remove(contact)
                print("Контакт успішно видалено.")
                return
        print("Контакт не знайдено.")

class NoteManager:
    def __init__(self):
        self.notes = []

    # Додає нову нотатку з опціональними тегами
    def add_note(self, content, tags=None):
        if tags is None:
            tags = []
        self.notes.append(Note(content=content, tags=tags))
        print("Нотатку успішно додано.")

    # Шукає нотатки, що містять певні ключові слова або теги
    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower() or keyword in note.tags]

    # Редагує вміст та теги існуючої нотатки
    def edit_note(self, index, new_content=None, new_tags=None):
        if 0 <= index < len(self.notes):
            if new_content:
                self.notes[index].content = new_content
            if new_tags is not None:
                self.notes[index].tags = new_tags
            print("Нотатку успішно оновлено.")
        else:
            print("Нотатку не знайдено.")

    # Видаляє нотатку зі списку нотаток
    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            print("Нотатку успішно видалено.")
        else:
            print("Нотатку не знайдено.")

def main():
    contacts = ContactBook()
    notes = NoteManager()

    while True:
        print("\nПерсональний Помічник")
        print("1. Додати контакт")
        print("2. Пошук контактів")
        print("3. Редагувати контакт")
        print("4. Видалити контакт")
        print("5. Показати дні народження")
        print("6. Додати нотатку")
        print("7. Пошук нотаток")
        print("8. Редагувати нотатку")
        print("9. Видалити нотатку")
        print("0. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == '1':
            name = input("Ім'я: ")
            address = input("Адреса: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            birthday_input = input("День народження (YYYY-MM-DD): ")
            try:
                birthday = datetime.strptime(birthday_input, "%Y-%m-%d")
                contact = Contact(name, address, phone, email, birthday)
                contacts.add_contact(contact)
            except ValueError:
                print("Некоректний формат дати.")
        
        elif choice == '2':
            name = input("Введіть ім'я для пошуку: ")
            found = contacts.search_contacts(name)
            if found:
                for c in found:
                    print(f"Ім'я: {c.name}, Адреса: {c.address}, Телефон: {c.phone}, Email: {c.email}, День народження: {c.birthday.strftime('%Y-%m-%d')}")
            else:
                print("Контакти не знайдено.")
        
        elif choice == '3':
            name = input("Введіть ім'я контакту для редагування: ")
            print("Введіть нові дані (залиште порожнім, щоб пропустити):")
            new_address = input("Нова адреса: ")
            new_phone = input("Новий телефон: ")
            new_email = input("Новий Email: ")
            new_birthday_input = input("Новий день народження (YYYY-MM-DD): ")
            kwargs = {}
            if new_address:
                kwargs['address'] = new_address
            if new_phone:
                kwargs['phone'] = new_phone
            if new_email:
                kwargs['email'] = new_email
            if new_birthday_input:
                try:
                    kwargs['birthday'] = datetime.strptime(new_birthday_input, "%Y-%m-%d")
                except ValueError:
                    print("Некоректний формат дати.")
            contacts.edit_contact(name, **kwargs)
        
        elif choice == '4':
            name = input("Введіть ім'я контакту для видалення: ")
            contacts.delete_contact(name)
        
        elif choice == '5':
            days = input("Введіть кількість днів для пошуку днів народження: ")
            if days.isdigit():
                upcoming = contacts.upcoming_birthdays(int(days))
                if upcoming:
                    for c in upcoming:
                        print(f"Ім'я: {c.name}, День народження: {c.birthday.strftime('%Y-%m-%d')}")
                else:
                    print("Немає днів народження в зазначений період.")
            else:
                print("Введено некоректну кількість днів.")
        
        elif choice == '6':
            content = input("Вміст нотатки: ")
            tags_input = input("Теги (через кому): ")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            notes.add_note(content, tags)
        
        elif choice == '7':
            keyword = input("Введіть ключове слово або тег для пошуку нотаток: ")
            found_notes = notes.search_notes(keyword)
            if found_notes:
                for idx, note in enumerate(found_notes):
                    print(f"{idx}. Вміст: {note.content}, Теги: {', '.join(note.tags)}")
            else:
                print("Нотатки не знайдено.")
        
        elif choice == '8':
            index = input("Введіть індекс нотатки для редагування: ")
            if index.isdigit():
                index = int(index)
                new_content = input("Новий вміст (залиште порожнім, щоб пропустити): ")
                new_tags_input = input("Нові теги (через кому, залиште порожнім, щоб пропустити): ")
                new_tags = [tag.strip() for tag in new_tags_input.split(",")] if new_tags_input else None
                notes.edit_note(index, new_content if new_content else None, new_tags)
            else:
                print("Невірний індекс.")
        
        elif choice == '9':
            index = input("Введіть індекс нотатки для видалення: ")
            if index.isdigit():
                notes.delete_note(int(index))
            else:
                print("Невірний індекс.")
        
        elif choice == '0':
            print("Вихід з програми.")
            break
        
        else:
            print("Невірна опція. Спробуйте знову.")

if __name__ == "__main__":
    main()