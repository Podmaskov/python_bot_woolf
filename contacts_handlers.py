from models import Contact
from datetime import datetime
from colorama import Fore

def handle_add_contact(contacts):
    name = input("Ім'я: ").strip()
    while not name:
        print(Fore.RED + "Ім'я не може бути порожнім.")
        name = input(Fore.YELLOW + "Ім'я: ").strip()

    address = input("Адреса (можна залишити порожнім): ").strip()

    phone = input("Телефон (в форматі +1234567890): ").strip()
    while not contacts.validate_phone(phone):
        print(Fore.RED + "Некоректний номер телефону. Спробуйте ще раз.")
        phone = input(Fore.YELLOW + "Телефон (в форматі +1234567890): ").strip()

    email = input("Email: ").strip()
    while not contacts.validate_email(email):
        print(Fore.RED + "Некоректний email. Спробуйте ще раз.")
        email = input(Fore.YELLOW + "Email: ").strip()

    birthday_input = input("День народження (DD-MM-YYYY): ").strip()
    birthday = None
    while not birthday:
        try:
            birthday = datetime.strptime(birthday_input, "%d-%m-%Y")
        except ValueError:
            print(Fore.RED + "Некоректний формат дати. Спробуйте ще раз.")
            birthday_input = input(Fore.YELLOW + "День народження (DD-MM-YYYY): ").strip()

    contact = Contact(name, address, phone, email, birthday)
    contacts.add_contact(contact)
    print(Fore.GREEN + "Контакт успішно додано!")

def handle_search_contacts(contacts):
    search_type = input("Шукати за (1: ім'я, 2: телефон, 3: email): ").strip()
    if search_type == '1':
        query = input("Введіть ім'я: ").strip()
        found = contacts.search_contacts(query)
    elif search_type == '2':
        query = input("Введіть телефон: ").strip()
        found = [c for c in contacts.contacts if query in c.phone]
    elif search_type == '3':
        query = input("Введіть email: ").strip()
        found = [c for c in contacts.contacts if query in c.email]
    else:
        print(Fore.RED + "Некоректний вибір.")
        return

    if found:
        for c in found:
            print(Fore.GREEN + f"Ім'я: {c.name}, Телефон: {c.phone}, Email: {c.email}")
    else:
        print(Fore.RED + "Контакти не знайдено.")

def handle_edit_contact(contacts):
    name = input("Введіть ім'я контакту для редагування: ").strip()
    if not name:
        print(Fore.RED + "Ім'я не може бути порожнім.")
        return

    contact = next((c for c in contacts.contacts if c.name.lower() == name.lower()), None)
    if not contact:
        print(Fore.RED + "Контакт не знайдено.")
        return

    print(Fore.YELLOW + f"\nПоточні дані контакту:")
    print(Fore.CYAN + f"Ім'я: {contact.name}")
    print(Fore.CYAN + f"Адреса: {contact.address}")
    print(Fore.CYAN + f"Телефон: {contact.phone}")
    print(Fore.CYAN + f"Email: {contact.email}")
    print(Fore.CYAN + f"День народження: {contact.birthday.strftime('%d-%m-%Y')}")


    print(Fore.YELLOW + "\nВведіть нові дані (залиште порожнім, щоб пропустити):")

    new_address = input("Нова адреса: ").strip()

    new_phone = None
    while True:
        phone_input = input("Новий телефон (в форматі +1234567890, залиште порожнім, щоб пропустити): ").strip()
        if not phone_input:
            break
        if contacts.validate_phone(phone_input):
            new_phone = phone_input
            break
        else:
            print(Fore.RED + "Некоректний номер телефону. Спробуйте ще раз.")

    new_email = None
    while True:
        email_input = input("Новий Email (залиште порожнім, щоб пропустити): ").strip()
        if not email_input:
            break
        if contacts.validate_email(email_input):
            new_email = email_input
            break
        else:
            print(Fore.RED + "Некоректний email. Спробуйте ще раз.")

    new_birthday = None
    while True:
        birthday_input = input("Новий день народження (DD-MM-YYYY, залиште порожнім, щоб пропустити): ").strip()
        if not birthday_input:
            break
        try:
            new_birthday = datetime.strptime(birthday_input, "%d-%m-%Y")
            break
        except ValueError:
            print(Fore.RED + "Некоректний формат дати. Спробуйте ще раз.")

    kwargs = {}
    if new_address:
        kwargs['address'] = new_address
    if new_phone:
        kwargs['phone'] = new_phone
    if new_email:
        kwargs['email'] = new_email
    if new_birthday:
        kwargs['birthday'] = new_birthday

    if kwargs:
        contacts.edit_contact(name, **kwargs)
        print(Fore.GREEN + "Контакт успішно оновлено.")
    else:
        print(Fore.YELLOW + "Не внесено жодних змін.")

def handle_delete_contact(contacts):
    name = input("Введіть ім'я контакту для видалення: ").strip()
    if not name:
        print(Fore.RED + "Ім'я не може бути порожнім.")
        return

    success, message = contacts.delete_contact(name)
    if success:
        print(Fore.GREEN + message)
    else:
        print(Fore.RED + message)

def handle_show_birthdays(contacts):
    days_input = input("Введіть кількість днів для пошуку днів народження: ").strip()
    if not days_input.isdigit():
        print(Fore.RED + "Введено некоректну кількість днів.")
        return

    days = int(days_input)
    upcoming = contacts.upcoming_birthdays(days)
    if upcoming:
        print(Fore.GREEN + "Дні народження в найближчі дні:")
        for c in upcoming:
            print(Fore.GREEN + f"Ім'я: {c.name}, День народження: {c.birthday.strftime('%Y-%m-%d')}")
    else:
        print(Fore.RED + "Немає днів народження в зазначений період.")

