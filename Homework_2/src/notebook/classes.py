from datetime import datetime
from abc import ABC, abstractmethod
from prettytable import PrettyTable


class Note():

    def __init__(self, name, text, tags=None):
        self.createde_time = datetime.now()
        self.name = name
        self.text = text
        self.tags = set()
        if tags:
            self.tags.update(tags)


    def add_tags(self, tags):
        self.tags.update(tags)

    def change_tags(self, new_tags):
        self.tags = set([*new_tags])

    def change_note(self, new_value):
        self.text = new_value

    def clean_tag(self):
        self.tags = set()

    def __eq__(self, obj: object) -> bool:
        return self.createde_time == obj.createde_time
    
    def __ge__(self, obj):
        return self.createde_time >= obj.createde_time
    
    def __le__(self, obj):
        return self.createde_time <= obj.createde_time
    
    def __lt__(self, obj):
        return self.createde_time < obj.createde_time
    
    def __gt__(self, obj):
        return self.createde_time > obj.createde_time


class NoteBook():

    def __init__(self):
        self.data = []

    def add_note(self, name, value):
        new_note = Note(name, value)
        self.data.append(new_note)
        return new_note

    def add(self, note: Note):
        self.data.append(note)

    def show_all(self):
        return NoteInterface().show_table(self.data)
    
    def search(self, value):

        result = []
        for note in self.data:
            
            if value in note.tags or value in note.name:
                result.append(note)

        for note in result:
            if note.name == value:
                result = [note]

        return result if value else []
    
    def delete(self, note):
        for i in self.data:
            if i == note:
                del self.data[self.data.index(note)]


    def change(self, new_value, note):
        self.delete(note) 
        self.add_note(note.name, new_value)

    def change_tag(self, new_tags, note):
        for n in self.data:
            if n.name == note.name:
                index_note = self.data.index(n)
                old_note = self.data[index_note]
                new_note = Note(old_note.name, old_note.text, new_tags)
                
                self.delete(old_note)
                self.add(new_note)
        

class Interface(ABC):

    @abstractmethod
    def show_table(self, list_of_notes):
        pass

    @abstractmethod
    def show_help_table(self):
        pass


class NoteInterface(Interface):

    def show_table(self, list_of_notes):
        table = PrettyTable(['Назва', 'Теги', 'Нотатка'])

        for note in list_of_notes:
            if len(note.text) > 100: # Для великих нотаток кожні 100 символів додаємо \n (для гарного виводу)
                note_tags = ', '.join(note.tags)
                
                text = ''
                counter = 0
                for i in note.text:
                    text += i
                    counter += 1
                    if not counter % 100:
                        text += '\n' 

                    if len(text) > 296:
                        text += '... '
                        break

                table.add_row([note.name, note_tags, text], divider=True)        

            else:
                note_tags = ', '.join(note.tags)
                table.add_row([note.name, note_tags, note.text], divider=True)
        
        return table
    
    def show_help_table(self):
        HELP_TABLE = PrettyTable(['Команди', 'Пояснення'])
        HELP_TABLE.add_row(['add <назва нотатки> <текс нотатки>', 'створити нову нотатку (назва без пробілів)',], divider=True)
        HELP_TABLE.add_row(['show <date|alp|size>', "вивести всі нотатки, сортувати за датою|алфавітом|розміром (не обов'язково)"], divider=True)
        HELP_TABLE.add_row(['search <тег|назва нотатки>', 'пошук нотатки за тегами або назвою нотатки'], divider=True)
        HELP_TABLE.add_row(['close', 'завершити роботу',], divider=True)
        HELP_TABLE.add_row(['help', 'список команд',], divider=True)
        return HELP_TABLE