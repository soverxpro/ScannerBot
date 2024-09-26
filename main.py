import os

def main_menu():
    while True:
        print("### Выберите что вы хотите запустить ###")
        print("1: Поиск поддоменов")
        print("2: Разрешение поддоменов в IP")
        print("3: Сканирование Nmap")
        print("4: Запуск Telegram-бота")
        print("5: Выход")

        choice = input("Введите номер выбора: ")

        if choice == '1':
            os.system('python3 scripts/script1_subdomain_finder.py')
        elif choice == '2':
            os.system('python3 scripts/script2_resolve_ip.py')
        elif choice == '3':
            os.system('python3 scripts/script3_nmap_scan.py')
        elif choice == '4':
            os.system('python3 scripts/script4_telegram_bot.py')
        elif choice == '5':
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main_menu()
