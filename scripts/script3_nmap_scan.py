#script3_nmap_scan.py
import nmap
import os
import time


def scan_nmap(ip_file, result_file):
    nm = nmap.PortScanner()
    scanned_ips = set()  # Множество для отслеживания отсканированных IP

    with open(ip_file, 'r') as ipf, open(result_file, 'w') as rf:
        ip_addresses = ipf.readlines()

        for line in ip_addresses:
            ip = line.split(': ')[1].strip()  # Получаем IP-адрес из строки

            # Проверка наличия IP в множестве
            if ip in scanned_ips:
                print(f"Пропускаем IP {ip}, так как он уже отсканирован.")
                continue  # Пропускаем повторное сканирование

            print(f"Сканирование Nmap для {ip} на всех 65535 TCP-портах с -T4")

            try:
                # Запускаем nmap сканирование всех 65535 TCP-портов с опцией -T4
                scan_result = nm.scan(ip, '1-65535', arguments='-T4')

                # Сохраняем результаты
                for proto in nm[ip].all_protocols():  # Проверяем все протоколы
                    lport = nm[ip][proto].keys()  # Получаем список всех портов
                    for port in lport:
                        state = nm[ip][proto][port]['state']
                        rf.write(f"{ip} Port: {port} State: {state}\n")
                        print(f"{ip} Port: {port} State: {state}")

                # Добавляем IP в множество, чтобы избежать повторного сканирования
                scanned_ips.add(ip)

            except KeyboardInterrupt:
                print("\nСканирование прервано пользователем.")
                break  # Прерываем цикл, если пользователь нажал Ctrl+C

            except Exception as e:
                print(f"Ошибка при сканировании {ip}: {e}")

    print(f"Результаты Nmap сохранены в {result_file}")


if __name__ == "__main__":
    ip_file_path = 'data/ip_addresses.txt'
    result_file_path = 'data/nmap_results.txt'

    if not os.path.exists('data'):
        os.makedirs('data')

    scan_nmap(ip_file_path, result_file_path)
