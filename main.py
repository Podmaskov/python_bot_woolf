from contact_book import ContactBook
from note_manager import NoteManager
from models import Contact
from models import Note
from datetime import datetime
from colorama import Fore, Style, init

# Ініціалізація Colorama
init(autoreset=True)

def main():
    contacts = ContactBook()
    notes = NoteManager()

    while True:
        print(Fore.CYAN + "\nПерсональний Помічник")
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

        choice = input(Fore.YELLOW + "Виберіть опцію: ")

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
                print(Fore.GREEN + "Контакт успішно додано.")
            except ValueError:
                print(Fore.RED + "Некоректний формат дати.")
        
        elif choice == '2':
            name = input("Введіть ім'я для пошуку: ")
            found = contacts.search_contacts(name)
            if found:
                for c in found:
                    print(Fore.GREEN + f"Ім'я: {c.name}, Адреса: {c.address}, Телефон: {c.phone}, Email: {c.email}, День народження: {c.birthday.strftime('%Y-%m-%d')}")
            else:
                print(Fore.RED + "Контакти не знайдено.")
        
        elif choice == '3':
            name = input("Введіть ім'я контакту для редагування: ")
            print(Fore.YELLOW + "Введіть нові дані (залиште порожнім, щоб пропустити):")
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
                    print(Fore.RED + "Некоректний формат дати.")
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
                        print(Fore.GREEN + f"Ім'я: {c.name}, День народження: {c.birthday.strftime('%Y-%m-%d')}")
                else:
                    print(Fore.RED + "Немає днів народження в зазначений період.")
            else:
                print(Fore.RED + "Введено некоректну кількість днів.")
        
        elif choice == '6':
            content = input("Вміст нотатки: ")
            tags_input = input("Теги (через кому): ")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            notes.add_note(content, tags)
            print(Fore.GREEN + "Нотатку успішно додано.")
        
        elif choice == '7':
            keyword = input("Введіть ключове слово або тег для пошуку нотаток: ")
            found_notes = notes.search_notes(keyword)
            if found_notes:
                for idx, note in enumerate(found_notes):
                    print(Fore.GREEN + f"{idx}. Вміст: {note.content}, Теги: {', '.join(note.tags)}")
            else:
                print(Fore.RED + "Нотатки не знайдено.")
        
        elif choice == '8':
            index = input("Введіть індекс нотатки для редагування: ")
            if index.isdigit():
                index = int(index)
                new_content = input("Новий вміст (залиште порожнім, щоб пропустити): ")
                new_tags_input = input("Нові теги (через кому, залиште порожнім, щоб пропустити): ")
                new_tags = [tag.strip() for tag in new_tags_input.split(",")] if new_tags_input else None
                notes.edit_note(index, new_content if new_content else None, new_tags)
            else:
                print(Fore.RED + "Невірний індекс.")
        
        elif choice == '9':
            index = input("Введіть індекс нотатки для видалення: ")
            if index.isdigit():
                notes.delete_note(int(index))
                print(Fore.GREEN + "Нотатку успішно видалено.")
            else:
                print(Fore.RED + "Невірний індекс.")
        
        elif choice == '0':
            print(Fore.CYAN + "Вихід з програми.")
            break
        
        else:
            print(Fore.RED + "Невірна опція. Спробуйте знову.")

if __name__ == "__main__":
    main()