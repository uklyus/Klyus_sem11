import csv
from dataclasses import dataclass
from datetime import datetime
import json
import os
from typing import List


prioritets = ['Низкий', 'Средний', 'Высокий']


@dataclass
class Note:
    id: int
    title: str
    content: str
    timestamp: str

    @property
    def json(self) :
        return self.__dict__

    def __str__(self):
        return self.title
    
    @property
    def view(self):
        return (f'ID: {self.id}\n'
                f'Заголовок: {self.title}\n'
                f'Контент: \n{self.content}\n'
                f'Дата создания: {self.timestamp}'
                )


class NoteCore:
    def __init__(self, core):
        self.core = core
        self.notes = list()
        self.load_notes()

    def load_notes(self):
        if os.path.isfile('notes.json'):
            with open("notes.json", "r") as file:
                self.notes = list(Note(**item) for item in json.load(file))

    def save_notes(self):
        with open ("notes.json", "w") as file:
            json.dump ([note.json for note in self.notes], file)
        
    def create_note(self):
        title = input('Введите название: ')
        print('Начните вводить заметку, а когда закончите отправьте 0')
        content = list()
        while (content_part := input()) != '0':
            content.append(content_part)
        if self.notes:
            note_id = max(int(item.id) for item in self.notes) + 1
        else:
            note_id = 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = Note(
            id=note_id,
            title=title,
            content='\n'.join(content),
            timestamp=timestamp
        )
        self.notes.append(note)
        self.save_notes()
        self.menu()

    def list_notes(self):
        if self.notes:
            print('Выберите заметку: ')
            for ind, note in enumerate(self.notes, start=1):
                print(f'{ind}. {str(note)}')
            print()
            note = None
            while True:
                try:
                    ind = int(input('Введите номер заметки: '))
                    note = self.notes[ind - 1]
                    break
                except Exception:
                    print('Это не похоже на номер')
            self.info_note(note)
        else:
            print('Пока нет заметок')
            self.menu()

        
    def info_note(self, note):
        print('\n' + '-' * 10)
        print(note.view)
        print('-' * 10 + '\n')
        ind=-1
        while True:
            try:
                print('1. Редактировать заметку \n'
                      '2. Удалить заметку \n'
                      '3. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 3 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.edit_note(note)
        elif ind == 2:
            self.delete_note(note)
        else:
            self.menu()


    def edit_note(self, note):
        while True:
            try:
                print('1. Изменить название \n'
                      '2. Изменить содержание')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            title = input()
            note.title = title
        else:
            print('Начните вводить заметку, а когда закончите отправьте 0')
            content = list()
            while (content_part := input()) != '0':
                content.append(content_part)
            note.content = '\n'.join(content)

        self.save_notes()
        self.menu()

    def delete_note(self, note):
        while True:
            try:
                print('Вы уверены, что хотите удалить? \n'
                      '1. Да \n'
                      '2. Нет ')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
            
        if ind == 1:
            self.notes.remove(note)
        else:
            self.info_note(note)
        self.save_notes()
        self.menu()

    def import_notes(self):
        while True:
            try:
                filepath = input('Укажите путь до файла: ')
                with open(filepath, 'r') as file:
                    reader = csv.DictReader(file)
                    notes = list()
                    for item in reader:
                        if set(item.keys()) != {'id', 'title', 'content', 'timestamp'}:
                            print('Ошибка входного файла')
                            raise ValueError()
                        else:
                            notes.append(Note(**item))
                self.notes += notes
                print('Заметки успешно импортированы из CSV-файла.')
                break
            except Exception:
                print('Это не похоже на путь до файла')
        self.save_notes()
        self.menu()

    def export_notes(self):
        filepath = input('Укажите название для файла: ')
        with open(f'{filepath}.csv', 'a+', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'title', 'content', 'timestamp'])
            for note in self.notes:
                writer.writerow([note.id, note.title, note.content, note.timestamp])
        print('Заметки успешно экспортированы из CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Создать заметку \n'
                      '2. Смотреть заметки \n'
                      '3. Импорт заметок \n'
                      '4. Экспорт заметок \n'
                      '5. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 5 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            self.create_note()
        elif ind == 2:
            self.list_notes()
        elif ind == 3:
            self.import_notes()
        elif ind == 4:
            self.export_notes()
        else:
            self.core.menu()


@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: int
    due_date: str
    done: bool = False

    @property
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }
    
    def __str__(self):
        return f'{self.title} - {"Выполнена" if self.done else "В работе"} - {prioritets[self.priority]} - {self.due_date}'
    
    @property
    def view(self):
        return (f'ID: {self.id}\n'
                f'Заголовок: {self.title}\n'
                f'Описание: {self.description}\n'
                f'Статус: {"Выполнена" if self.done else "В работе"}\n'
                f'Приоритет: {prioritets[self.priority]}\n'
                f'Срок выполнения: {self.due_date}')
    
    def __lt__(self, other):
        return self.priority < other.priority

class TaskCore:
    def __init__(self, core):
        self.tasks = list()
        self.core = core
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.isfile('tasks.json'):
            with open("tasks.json", "r") as file:
                self.tasks = list(Task(**item) for item in json.load(file))

    def save_tasks(self):
        with open ("tasks.json", "w") as file:
            json.dump ([task.json for task in self.tasks], file)

    def create_task(self):
        title = input('Введите название задачи: ')
        description = input('Введите описание задачи: ')

        while True:
            try:
                due_date = datetime.strptime(input('Введи срок выполнения задачи: '), "%d-%m-%Y")
                break
            except Exception:
                print('это не похоже на дату')

        while True:
            try:
                priority_str = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                priority = prioritets.index(priority_str)
                break
            except Exception:
                print('это не похоже на приоритет')

        if self.tasks:
            task_id = max(int(item.id) for item in self.tasks) + 1
        else:
            task_id = 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date.strftime('%d-%m-%Y'),
            priority=priority
        )
        self.tasks.append(task)
        self.save_tasks()
        self.menu()

    def list_tasks(self):
        if self.tasks:
            print('Выберите задачу: ')
            for ind, task in enumerate(sorted(self.tasks, reverse=True), start=1):
                print(f'{ind}. {str(task)}')
            print()
            task = None
            while True:
                try:
                    ind = int(input('Введите номер задачи: '))
                    task = self.tasks[ind - 1]
                    break
                except Exception:
                    print('Это не похоже на номер')
            self.info_task(task)

        else:
            print('Пока нет задач')
            self.menu()

    def info_task(self, task):
        print('\n' + '-' * 10)
        print(task.view)
        print('-' * 10 + '\n')
        ind=-1
        while True:
            try:
                print('1. Редактировать задачу \n'
                      '2. Удалить задачу \n'
                      '3. Отметить задачу как выполненную\n'
                      '4. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 4 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.edit_task(task)
        elif ind == 2:
            self.delete_task(task)
        elif ind == 3:
            self.mark_as_completed(task)
        else:
            self.menu()

    def edit_task(self, task):
        while True:
            try:
                print('1. Изменить название\n'
                    '2. Изменить описание\n'
                    '3. Изменить приоритет\n'
                    '4. Изменить дату завершения\n'
                    '5. Изменить статус выполнения')
                ind = int(input('Выберите действие: '))
                assert 1 <= ind <= 5
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт')
        
        if ind == 1:
            task.title = input('Введите новое название: ')
        elif ind == 2:
            task.description = input('Введите описание: ')
        elif ind == 3:
            while True:
                try:
                    priority = int(input('Введите новый приоритет: '))
                    task.priority = prioritets.index(priority) 
                    break
                except ValueError:
                    print('это не похоже на приоритет')
        elif ind == 4:
            while True:
                try:
                    due_date = datetime.strptime(input('Введи срок выполнения задачи: '), "%d-%m-%Y")
                    task.due_date = due_date.strftime("%d-%m-%Y")
                    break
                except Exception:
                    print('это не похоже на дату')
        elif ind == 5:
            while True:
                try:
                    status = input('Задача выполнена? (да/нет): ').strip().lower()
                    if status in ['да', 'нет']:
                        task.done = (status == 'да')
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print('Введите "да" или "нет".')
        
        self.save_tasks() 
        self.menu()

    def mark_as_completed(self, task):
        task.done = True
        print('Задача помечена как выполенная')
        self.menu()

    def delete_task(self, task):
        while True:
            try:
                print('Вы уверены, что хотите удалить? \n'
                      '1. Да \n'
                      '2. Нет ')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
            
        if ind == 1:
            self.tasks.remove(task)
        else:
            self.info_task(task)
        self.save_tasks()
        self.menu()

    def import_tasks(self):
        while True:
            try:
                filepath = input('Укажите путь до файла: ')
                with open(filepath, 'r') as file:
                    reader = csv.DictReader(file)
                    tasks = list()
                    for item in reader:
                        if set(item.keys()) != {'id', 'title', 'description', 'priority', 'due_date', 'done'}:
                            print('Ошибка входного файла')
                            raise ValueError()
                        else:
                            tasks.append(Task(**item))
                self.tasks += tasks
                print('Заметки успешно импортированы из CSV-файла.')
                break
            except Exception:
                print('Это не похоже на путь до файла')
        self.save_tasks()
        self.menu()

    def export_tasks(self):
        filepath = input('Укажите название для файла: ')
        with open(f'{filepath}.csv', 'a+', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'title', 'description', 'priority', 'due_date', 'done'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description,
                                 task.priority, task.due_date, task.done])
        print('Заметки успешно экспортированы из CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Создать задачу \n'
                      '2. Смотреть задачи \n'
                      '3. Импорт задач \n'
                      '4. Экспорт задач \n'
                      '5. Назад')
                ind = int(input('Выберите действие: '))
                assert ind <= 5 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')
        if ind == 1:
            self.create_task()
        elif ind == 2:
            self.list_tasks()
        elif ind == 3:
            self.import_tasks()
        elif ind == 4:
            self.export_tasks()
        else:
            self.core.menu()


@dataclass
class Contact:
    id: int
    name: str
    phone: str
    email: str

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    def __str__(self):
        return f'{self.name} - {self.phone} - {self.email}'

class ContactCore:
    def __init__(self, core):
        self.contacts = list()
        self.core = core
        self.load_contacts()

    def load_contacts(self):
        if os.path.isfile('contacts.json'):
            with open("contacts.json", "r") as file:
                self.contacts = [Contact(**item) for item in json.load(file)]

    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump([contact.json for contact in self.contacts], file)

    def create_contact(self):
        name = input('Введите имя контакта: ')
        phone = input('Введите номер телефона: ')
        email = input('Введите адрес электронной почты: ')

        if self.contacts:
            contact_id = max(int(contact.id) for contact in self.contacts) + 1
        else:
            contact_id = 1

        contact = Contact(
            id=contact_id,
            name=name,
            phone=phone,
            email=email
        )
        self.contacts.append(contact)
        self.save_contacts()
        self.menu()

    def search_contact(self):
        query = input('Введите имя или номер телефона для поиска: ')
        found_contacts = [contact for contact in self.contacts if query in contact.name or query in contact.phone]
        
        if found_contacts:
            print('Найденные контакты:')
            for contact in found_contacts:
                print(contact)
        else:
            print('Контакты не найдены.')
        self.menu()

    def list_contacts(self):
        if self.contacts:
            print('Список контактов:')
            for ind, contact in enumerate(self.contacts, start=1):
                print(f'{ind}. {str(contact)}')
            print()
            contact = None
            while True:
                try:
                    ind = int(input('Введите номер контакта для редактирования: '))
                    contact = self.contacts[ind - 1]
                    break
                except Exception:
                    print('Это не похоже на номер')
            self.info_contact(contact)
        else:
            print('Пока нет контактов')
            self.menu()

    def info_contact(self, contact):
        print('\n' + '-' * 10)
        print(contact)
        print('-' * 10 + '\n')
        ind = -1
        while True:
            try:
                print('1. Редактировать контакт \n'
                      '2. Удалить контакт \n'
                      '3. Назад')
                ind = int(input('Выберите действие: '))
                assert 1 <= ind <= 3
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.edit_contact(contact)
        elif ind == 2:
            self.delete_contact(contact)
        else:
            self.menu()

    def edit_contact(self, contact):
        while True:
            try:
                print('1. Изменить имя\n'
                      '2. Изменить номер телефона\n'
                      '3. Изменить адрес электронной почты')
                ind = int(input('Выберите действие: '))
                assert 1 <= ind <= 3
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт')

        if ind == 1:
            contact.name = input('Введите новое имя: ')
        elif ind == 2:
            contact.phone = input('Введите новый номер телефона: ')
        elif ind == 3:
            contact.email = input('Введите новый адрес электронной почты: ')

        self.save_contacts()
        self.menu()

    def delete_contact(self, contact):
        while True:
            try:
                print('Вы уверены, что хотите удалить? \n'
                      '1. Да \n'
                      '2. Нет ')
                ind = int(input('Выберите действие: '))
                assert ind <= 2 and ind >= 1
                break
            except Exception:
                print('Это не похоже на цифру')

        if ind == 1:
            self.contacts.remove(contact)
        else:
            self.info_contact(contact)
        self.save_contacts()
        self.menu()

    def import_contacts(self):
        while True:
            try:
                filepath = input('Укажите путь до файла: ')
                with open(filepath, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    contacts = list()
                    for item in reader:
                        if set(item.keys()) != {'id', 'name', 'phone', 'email'}:
                            print('Ошибка входного файла')
                            raise ValueError()
                        else:
                            contacts.append(Contact(**item))
                self.contacts += contacts
                print('Контакты успешно импортированы из CSV-файла.')
                break
            except Exception:
                print('Это не похоже на путь до файла')
        self.save_contacts()
        self.menu()

    def export_contacts(self):
        filepath = input('Укажите название для файла: ')
        with open(f'{filepath}.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'name', 'phone', 'email'])
            for contact in self.contacts:
                writer.writerow([contact.id, contact.name, contact.phone, contact.email])
        print('Контакты успешно экспортированы в CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Добавить контакт \n'
                      '2. Поиск контакта \n'
                      '3. Посмотреть контакты \n'
                      '4. Импорт контактов \n'
                      '5. Экспорт контактов \n'
                      '6. Назад')
                ind = int(input('Выберите действие: '))
                assert 1 <= ind <= 6
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт')

        if ind == 1:
            self.create_contact()
        elif ind == 2:
            self.search_contact()
        elif ind == 3:
            self.list_contacts()
        elif ind == 4:
            self.import_contacts()
        elif ind == 5:
            self.export_contacts()
        else:
            self.core.menu()


@dataclass
class FinanceRecord:
    id: int
    amount: float
    category: str
    date: str  # ДД-ММ-ГГГГ
    description: str

    @property
    def json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

class FinanceCore:
    def __init__(self, core):
        self.records: List[FinanceRecord] = []
        self.core = core
        self.load_records()

    def load_records(self):
        if os.path.isfile('finance.json'):
            with open("finance.json", "r") as file:
                self.records = [FinanceRecord(**item) for item in json.load(file)]

    def save_records(self):
        with open("finance.json", "w") as file:
            json.dump([record.json for record in self.records], file)

    def add_record(self):
        while True:
            try:
                amount = float(input('Введите сумму операции (положительное для доходов, отрицательное для расходов): '))
                if amount == 0:
                    raise ValueError("Сумма не может быть нулевой.")
                break
            except ValueError:
                print('Это не похоже на сумму. Попробуйте снова.')

        category = input('Введите категорию операции: ')
        while True:
            try:
                date_str = input('Введите дату операции (ДД-ММ-ГГГГ): ')
                date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%d-%m-%Y")
                break
            except ValueError:
                print('Неверный формат даты. Попробуйте снова.')

        description = input('Введите описание операции: ')

        record_id = max((record.id for record in self.records), default=0) + 1
        record = FinanceRecord(
            id=record_id,
            amount=amount,
            category=category,
            date=date,
            description=description
        )
        self.records.append(record)
        self.save_records()
        print('Финансовая запись добавлена.')
        self.menu()

    def view_records(self):
        if not self.records:
            print('Нет финансовых записей.')
            self.menu()
            return

        filter_option = input('Хотите отфильтровать по дате или категории? (дата/категория/нет): ').strip().lower()
        filtered_records = self.records

        if filter_option == 'дата':
            date_str = input('Введите дату для фильтрации (ДД-ММ-ГГГГ): ')
            filtered_records = [record for record in self.records if record.date == date_str]
        elif filter_option == 'категория':
            category = input('Введите категорию для фильтрации: ')
            filtered_records = [record for record in self.records if record.category.lower() == category.lower()]

        if filtered_records:
            print('Финансовые записи:')
            for record in filtered_records:
                print(f'ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}')
        else:
            print('Нет записей, соответствующих критериям фильтрации.')

        self.menu()

    def generate_report(self):
        start_date_str = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
        end_date_str = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

        report_records = [record for record in self.records if start_date <= datetime.strptime(record.date, "%d-%m-%Y") <= end_date]

        total_income = sum(record.amount for record in report_records if record.amount > 0)
        total_expense = sum(record.amount for record in report_records if record.amount < 0)
        balance = total_income + total_expense

        print(f'Отчет за период с {start_date_str} по {end_date_str}:')
        print(f'Общий доход: {total_income}')
        print(f'Общие расходы: {total_expense}')
        print(f'Баланс: {balance}')

        self.menu()
    
    def import_records(self):
        while True:
            try:
                filepath = input('Укажите путь до файла для импорта (CSV): ')
                with open(filepath, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    records = []
                    for item in reader:
                        if set(item.keys()) != {'id', 'amount', 'category', 'date', 'description'}:
                            print('Ошибка входного файла. Убедитесь, что он имеет правильный формат.')
                            raise ValueError()
                        item['amount'] = float(item['amount'])
                        records.append(FinanceRecord(**item))
                    self.records.extend(records)
                    print('Финансовые записи успешно импортированы из CSV-файла.')
                    break
            except Exception as e:
                print(f'Ошибка: {e}. Попробуйте снова.')
        self.save_records()
        self.menu()

    def export_records(self):
        filepath = input('Укажите название файла для экспорта (без расширения): ')
        with open(f'{filepath}.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['id', 'amount', 'category', 'date', 'description'])
            for record in self.records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])
        print('Финансовые записи успешно экспортированы в CSV-файл.')
        self.menu()

    def menu(self):
        while True:
            try:
                print('1. Добавить финансовую запись')
                print('2. Просмотреть финансовые записи')
                print('3. Сгенерировать отчет')
                print('4. Импортировать финансовые записи')
                print('5. Экспортировать финансовые записи')
                print('6. Назад')
                choice = int(input('Выберите действие: '))
                assert 1 <= choice <= 6
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт.')

        if choice == 1:
            self.add_record()
        elif choice == 2:
            self.view_records()
        elif choice == 3:
            self.generate_report()
        elif choice == 4:
            self.import_records()
        elif choice == 5:
            self.export_records()
        else:
            self.core.menu()



class Calc:
    def __init__(self, core):
        self.core = core

    def menu(self):
        while True:
            try:
                print('1. Посчитать выражение')
                print('2. Назад')

                choice = int(input('Выберите действие: '))
                assert 1 <= choice <= 2
                break
            except Exception:
                print('Это не похоже на цифру или выбран недопустимый пункт.')

        if choice == 1:
            try:
                request = input('Напишите выражение: ')
                if set(request) > set('0123456789.-+*/'):
                    raise ValueError()
                print(f'Результат: {eval(request)}')
            except ValueError:
                print('неизвестный метод')
            except ZeroDivisionError:
                print('нельзя делить на ноль')
            self.menu()
        else:
            self.core.menu()
    
class Core:
    def __init__(self):
        self.note = NoteCore(self)
        self.task = TaskCore(self)
        self.contact = ContactCore(self)
        self.finance = FinanceCore(self)
        self.calc = Calc(self)

    def menu(self):
        while True:
            print('Добро пожаловать в Персональный помощник!')
            print('Выберите действие:')
            print('1. Управление заметками')
            print('2. Управление задачами')
            print('3. Управление контактами')
            print('4. Управление финансовыми записями')
            print('5. Калькулятор')
            print('6. Выход')

            try:
                choice = int(input('Введите номер действия: '))
                if choice == 1:
                    self.note.menu()
                elif choice == 2:
                    self.task.menu()
                elif choice == 3:
                    self.contact.menu()
                elif choice == 4:
                    self.finance.menu()
                elif choice == 5:
                    self.calc.menu()
                elif choice == 6:
                    print('Выход из программы.')
                    exit(0)
                else:
                    print('Неверный выбор. Пожалуйста, выберите номер от 1 до 6.')
            except ValueError:
                print('Это не похоже на цифру. Попробуйте снова.')

if __name__ == '__main__':
    core = Core()
    core.menu()