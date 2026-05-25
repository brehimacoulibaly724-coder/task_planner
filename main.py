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
        print(f"❌ Erreur: date '{date}' pas au format YYYY-MM-DD")
        return

    if priority not in PRIORITIES:
        print(f"❌ Erreur: priorité doit être low/medium/high")
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
    print(f"✅ Tâche {task_id} ajoutée: {description}")


def list_tasks(tasks):
    if not tasks:
        print("📭 Aucune tâche.")
        return

    sorted_tasks = sorted(tasks, key=lambda t: (t["date"], PRIORITIES[t["priority"]]))

    print("\n📋 LISTE DES TÂCHES:")
    for task in sorted_tasks:
        status = "✅" if task["done"] else "⬜"
        print(f"{status} [{task['id']}] {task['description']} | {task['date']} ({task['priority']})")
    print(f"Total: {len(tasks)} tâches, terminées: {sum(1 for t in tasks if t['done'])}\n")


def mark_done(tasks, task_number):
    try:
        task_num = int(task_number)
    except ValueError:
        print("❌ Numéro invalide")
        return

    for task in tasks:
        if task["id"] == task_num:
            task["done"] = True
            print(f"🎉 Tâche {task_num} terminée !")
            return
    print(f"❌ Tâche {task_num} non trouvée")


def delete_task(tasks, task_number):
    try:
        task_num = int(task_number)
    except ValueError:
        print("❌ Numéro invalide")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_num:
            tasks.pop(i)
            for idx, t in enumerate(tasks, 1):
                t["id"] = idx
            print(f"🗑️ Tâche {task_num} supprimée")
            return
    print(f"❌ Tâche {task_num} non trouvée")


def show_help():
    print("""
COMMANDES:
  add <description> <YYYY-MM-DD> <low/medium/high>
  list
  done <numéro>
  delete <numéro>
  exit
""")


def main():
    print("📅 PLANIFICATEUR DE TÂCHES")
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
                print("💾 Sauvegardé. Au revoir !")
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
                print("❌ Commande invalide. Tapez 'help'")

        except KeyboardInterrupt:
            save_tasks(tasks)
            sys.exit(0)


if __name__ == "__main__":
    main()
