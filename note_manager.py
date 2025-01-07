import json
from models import Note
from colorama import Fore, Style

class NoteManager:
    def __init__(self, filename="notes.json"):
        self.notes = []
        self.filename = filename
        self.load_notes()

    # Додає нову нотатку з опціональними тегами
    def add_note(self, content, tags=None):
        if tags is None:
            tags = []
        self.notes.append(Note(content=content, tags=tags))
        self.save_notes()
        print(Fore.GREEN + "Нотатку успішно додано!" + Style.RESET_ALL)

    # Зберігає нотатку у файл
    def save_notes(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([note.to_dict() for note in self.notes], file, ensure_ascii=False, indent=4)

    # Завантажує нататки з файлу
    def load_notes(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.notes = [Note.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = []
            print(Fore.YELLOW + "Файл нотаток не знайдено або пошкоджений. Створено новий список нотаток." + Style.RESET_ALL)

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
            self.save_notes()
            print(Fore.GREEN + "Нотатку успішно оновлено!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Нотатку не знайдено." + Style.RESET_ALL)

    # Видаляє нотатку зі списку нотаток
    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_notes()
            print(Fore.GREEN + "Нотатку успішно видалено!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Нотатку не знайдено." + Style.RESET_ALL)