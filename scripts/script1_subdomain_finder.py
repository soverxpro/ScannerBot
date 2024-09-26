#script1_subdomain_finder.py
import sublist3r
import os
import time

def find_subdomains(domain_file, subdomain_file):
    with open(domain_file, 'r') as df:
        domains = df.readlines()
        for domain in domains:
            domain = domain.strip()

            # Указываем поисковые движки для Sublist3r
            engines = 'baidu,bing,yahoo,ask,netcraft,dnsdumpster,virustotal,threatcrowd,ssl,pdns'

            print(f"Поиск поддоменов для {domain} с использованием движков: {engines}")

            # Запускаем Sublist3r для поиска поддоменов
            try:
                subdomains = sublist3r.main(
                    domain,
                    40,  # Количество потоков
                    ports=None,
                    silent=False,  # Отключаем режим без вывода в консоль
                    verbose=True,  # Включаем подробный вывод
                    enable_bruteforce=False,  # Не включаем брутфорс
                    savefile=None,  # Сохраняем поддомены вручную
                    engines=engines  # Передаем движки для поиска
                )

                if subdomains:
                    print(f"Найденные поддомены для {domain}: {subdomains}")

                    # Сохраняем поддомены в файл, исключая поддомены с www
                    with open(subdomain_file, 'a') as sf:
                        for subdomain in subdomains:
                            if not subdomain.startswith('www.'):
                                print(f"Запись поддомена: {subdomain}")
                                sf.write(subdomain + '\n')
                            else:
                                print(f"Пропущен поддомен: {subdomain}")

                else:
                    print(f"Поддомены для {domain} не найдены.")

            except Exception as e:
                print(f"Ошибка при поиске поддоменов для {domain}: {e}")

            # Задержка между запросами для уменьшения нагрузки на поисковые движки
            time.sleep(5)

    print(f"Все поддомены сохранены в {subdomain_file}")

if __name__ == "__main__":
    # Пути к файлам доменов и поддоменов
    domain_file_path = 'data/domains.txt'
    subdomain_file_path = 'data/subdomains.txt'

    # Создание директории, если она не существует
    if not os.path.exists('data'):
        os.makedirs('data')

    # Запуск функции поиска поддоменов
    find_subdomains(domain_file_path, subdomain_file_path)
