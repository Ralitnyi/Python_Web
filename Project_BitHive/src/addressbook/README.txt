# Моя програма

Це проста програма для керування адресною книгою. Вона дозволяє додавати контакти, видаляти контакти, редагувати інформацію про контакти та переглядати список усіх контактів.

## Установка

1. Встановіть Python 3.11 на свій комп'ютер, якщо він ще не встановлений.
2. Завантажте або склонуйте репозиторій з програмою на свій комп'ютер.

## Запуск програми

1. Відкрийте командний рядок або термінал.
2. Перейдіть до каталогу з програмою.
3. Активуйте віртуальне середовище, якщо ви використовуєте його.
4. Запустіть програму за допомогою команди python task_main.py.

## Використання

Програма підтримує наступні команди:

- add: додати новий контакт до адресної книги. Приклад: add Mike 0960000000.
- email add: додати електронну адресу до контакту. Приклад: email add Mike mike@example.com.
- birthday add: додати дату народження до контакту. Приклад: birthday add Mike 01.01.1990.
- home add: додати адресу до контакту. Приклад: home add Mike Kyiv, Ukraine.
- change phone: змінити номер телефону контакту. Приклад: change phone Mike 0971111111.
- phone: вивести номер телефону контакту. Приклад: phone Mike.
- show all: вивести список усіх контактів.
- search: знайти контакт за ім'ям. Приклад: search Mike.
- delete phone: видалити номер телефону контакту. Приклад: delete phone Mike.
- delete birthday: видалити дату народження контакту. Приклад: delete birthday Mike.
- delete email: видалити електронну адресу контакту. Приклад: delete email Mike.
- delete contact: видалити контакт з адресної книги. Приклад: delete contact Mike.
- close, good bye, exit: завершити роботу програми.

## Залежності

Програма використовує наступні залежності, які повинні бути встановлені:

- tabulate:         для красивого виводу даних у вигляді таблиці.
- email-validator:  для перевірки валідності електронних адрес.
- phonenumbers:     для перевірки валідності телефонних номерів.
- Faker:            для додавання фейкових даних для тесту програми.

Встановіть залежності, виконавши команду pip install -r requirements.txt.

## Ліцензія

Ця програма поширюється за ліцензією MIT. Див. файл LICENSE для отримання додаткової інформації.