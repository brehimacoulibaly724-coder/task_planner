import json
import sys
from datetime import datetime

FILE_NAME = "tasks.json"
PRIORITIES = {"low": 3, "medium": 2, "high": 1}


def load_tasks():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(tasks, description, date, priority):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(f" Ошибка: дата '{date}' не в формате ГГГГ-ММ-ДД")
        return

    if priority not in PRIORITIES:
        print(f" Ошибка: приоритет должен быть low/medium/high")
        return

    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "description": description,
        "date": date,
        "priority": priority,
        "done": False
    }
    tasks.append(new_task)
    print(f" Задача {task_id} добавлена: {description}")


def list_tasks(tasks):
    if not tasks:
        print("📭 Нет задач.")
        return

    sorted_tasks = sorted(tasks, key=lambda t: (t["date"], PRIORITIES[t["priority"]]))

    print("\n📋 СПИСОК ЗАДАЧ:")
    print("-" * 50)
    for task in sorted_tasks:
        status = "" if task["done"] else "⬜"
        priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}[task["priority"]]
        print(f"{status} [{task['id']}] {task['description']} | {task['date']} {priority_icon}")
    print("-" * 50)
    print(f"Всего: {len(tasks)}, выполнено: {sum(1 for t in tasks if t['done'])}\n")


def mark_done(tasks, task_number):
    try:
        task_num = int(task_number)
    except ValueError:
        print(" Ошибка: номер должен быть числом")
        return

    for task in tasks:
        if task["id"] == task_num:
            if task["done"]:
                print(f" Задача {task_num} уже выполнена")
            else:
                task["done"] = True
                print(f"🎉 Задача {task_num} выполнена!")
            return
    print(f" Задача {task_num} не найдена")


def delete_task(tasks, task_number):
    try:
        task_num = int(task_number)
    except ValueError:
        print(" Ошибка: номер должен быть числом")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_num:
            tasks.pop(i)
            for idx, t in enumerate(tasks, 1):
                t["id"] = idx
            print(f" Задача {task_num} удалена")
            return
    print(f" Задача {task_num} не найдена")


def show_help():
    print("""
КОМАНДЫ:
  add <описание> <ГГГГ-ММ-ДД> <low/medium/high>  - добавить задачу
  list                                           - показать все задачи
  done <номер>                                   - отметить выполненной
  delete <номер>                                 - удалить задачу
  help                                           - справка
  exit                                           - выход
""")


def main():
    print("=" * 40)
    print(" ПЛАНИРОВЩИК ЗАДАЧ")
    print("=" * 40)
    print("Введите 'help' для справки\n")

    tasks = load_tasks()

    while True:
        try:
            user_input = input(">>> ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=3)
            command = parts[0].lower()

            if command == "exit":
                save_tasks(tasks)
                print(" Сохранено. До свидания!")
                sys.exit(0)
            elif command == "help":
                show_help()
            elif command == "list":
                list_tasks(tasks)
            elif command == "add" and len(parts) >= 4:
                add_task(tasks, parts[1], parts[2], parts[3].lower())
            elif command == "done" and len(parts) >= 2:
                mark_done(tasks, parts[1])
            elif command == "delete" and len(parts) >= 2:
                delete_task(tasks, parts[1])
            else:
                print(" Неверная команда. Введите 'help'")

        except KeyboardInterrupt:
            save_tasks(tasks)
            print("\n Сохранено. До свидания!")
            sys.exit(0)


if __name__ == "__main__":
    main()
