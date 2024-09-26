#script2_resolve_ip.py
import dns.resolver
import os

def resolve_ips(subdomain_file, ip_file):
    resolver = dns.resolver.Resolver()

    # Открываем файлы для чтения и записи
    with open(subdomain_file, 'r') as sf, open(ip_file, 'w') as ipf:
        subdomains = sf.readlines()

        for subdomain in subdomains:
            subdomain = subdomain.strip()
            print(f"Разрешение IP для {subdomain}")

            try:
                # Запрашиваем A-записи поддомена
                answers = resolver.resolve(subdomain, 'A')

                for rdata in answers:
                    ipf.write(f"{subdomain}: {rdata.to_text()}\n")
                    print(f"{subdomain}: {rdata.to_text()}")
            except Exception as e:
                print(f"Не удалось разрешить IP для {subdomain}: {e}")
    print(f"IP-адреса сохранены в {ip_file}")

if __name__ == "__main__":
    subdomain_file_path = 'data/subdomains.txt'
    ip_file_path = 'data/ip_addresses.txt'

    # Проверяем, существует ли директория, и создаём её, если нет
    if not os.path.exists('data'):
        os.makedirs('data')

    # Запускаем процесс разрешения IP-адресов
    resolve_ips(subdomain_file_path, ip_file_path)
