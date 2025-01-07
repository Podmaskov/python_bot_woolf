import json
from models import Note

class NoteManager:
    def __init__(self, filename="notes.json"):
        self.notes = []
        self.filename = filename
        self.load_notes()

    def add_note(self, content, tags=None):
        if tags is None:
            tags = []
        self.notes.append(Note(content=content, tags=tags))
        self.save_notes()
        print("Нотатку успішно додано.")

    def save_notes(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([note.to_dict() for note in self.notes], file, ensure_ascii=False, indent=4)

    def load_notes(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.notes = [Note.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = []

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower() or keyword in note.tags]

    def edit_note(self, index, new_content=None, new_tags=None):
        if 0 <= index < len(self.notes):
            if new_content:
                self.notes[index].content = new_content
            if new_tags is not None:
                self.notes[index].tags = new_tags
            self.save_notes()
            print("Нотатку успішно оновлено.")
        else:
            print("Нотатку не знайдено.")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_notes()
            print("Нотатку успішно видалено.")
        else:
            print("Нотатку не знайдено.")