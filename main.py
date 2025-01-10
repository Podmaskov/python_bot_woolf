from contact_book import ContactBook
from note_manager import NoteManager
from contacts_handlers import handle_add_contact, handle_search_contacts, handle_edit_contact, handle_delete_contact, handle_show_birthdays 
from notes_handlesrs import handle_add_note, handle_search_notes, handle_edit_note, handle_delete_note
from colorama import Fore, Back, Style, init

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
            print(
                Back.CYAN + "Введіть " +
                Fore.WHITE + Style.DIM + "'Exit'" +
                Back.CYAN + Style.NORMAL + " в будь-якому інпуті для виходу в головне меню.")
            handle_add_contact(contacts)
        
        elif choice == '2':
            handle_search_contacts(contacts)
        
        elif choice == '3':
            handle_edit_contact(contacts)

        
        elif choice == '4':
            handle_delete_contact(contacts)
        
        elif choice == '5':
           handle_show_birthdays(contacts)
        
        elif choice == '6':
            handle_add_note(notes)
        
        elif choice == '7':
            handle_search_notes(notes)
        
        elif choice == '8':
            handle_edit_note(notes)
        
        elif choice == '9':
            handle_delete_note(notes)
        
        elif choice == '0':
            print(Fore.CYAN + "Вихід з програми.")
            break
        
        else:
            print(Fore.RED + "Невірна опція. Спробуйте знову.")

if __name__ == "__main__":
    main()