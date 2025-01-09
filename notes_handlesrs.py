from colorama import Fore

def handle_add_note(notes):
    content = input("Вміст нотатки: ").strip()
    if not content:
        print(Fore.RED + "Вміст нотатки не може бути порожнім.")
        return

    tags_input = input("Теги (через кому): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    notes.add_note(content, tags)
    print(Fore.GREEN + "Нотатку успішно додано.")

def handle_search_notes(notes):
    keyword = input("Введіть ключове слово або тег для пошуку нотаток: ").strip()
    if not keyword:
        print(Fore.RED + "Ключове слово не може бути порожнім.")
        return

    found_notes = notes.search_notes(keyword)
    if found_notes:
        print(Fore.GREEN + "Знайдені нотатки:")
        for idx, note in enumerate(found_notes):
            print(Fore.GREEN + f"{idx}. Вміст: {note.content}, Теги: {', '.join(note.tags)}")
    else:
        print(Fore.RED + "Нотатки не знайдено.")

def handle_edit_note(notes):
    index_input = input("Введіть індекс нотатки для редагування: ").strip()
    if not index_input.isdigit():
        print(Fore.RED + "Невірний індекс.")
        return

    index = int(index_input)
    new_content = input("Новий вміст (залиште порожнім, щоб пропустити): ").strip()
    new_tags_input = input("Нові теги (через кому, залиште порожнім, щоб пропустити): ").strip()
    new_tags = [tag.strip() for tag in new_tags_input.split(",")] if new_tags_input else None

    notes.edit_note(index, new_content if new_content else None, new_tags)

def handle_delete_note(notes):
    index_input = input("Введіть індекс нотатки для видалення: ").strip()
    if not index_input.isdigit():
        print(Fore.RED + "Невірний індекс.")
        return

    index = int(index_input)
    notes.delete_note(index)
    print(Fore.GREEN + "Нотатку успішно видалено.")
