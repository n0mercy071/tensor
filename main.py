from html_parser import Parser
import argparse
import os


def create_path(url):
    '''Принимает строку url, возвращает строку пути и создает директории'''
    path = './' + url.split('//')[1]
    if path.find('www.') != -1:
        path = path.replace('www.', '')
    if path[len(path) - 1] != '/':
        last_slash_pos = path.rfind('/')
        path = path[:last_slash_pos + 15] + '/'

    if not os.path.isdir(path):
        os.makedirs(path)

    return path + 'index.txt'


def save_text(url):
    '''Принимает строку url, сохраняет текст из страницы'''
    text = parser.get_text_url(url)
    if not text:
        print('Не удалось скачать страницу')
    else:
        path = create_path(url)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(text)

        print('Готово.\nПуть: ' + path)


def create_argparser():
    '''Создает парсем аргументов командной строки'''
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?')

    return parser


if __name__ == '__main__':
    parser = Parser()
    argparser = create_argparser()
    namespace = argparser.parse_args()

    if namespace.url:
        save_text(namespace.url)
    else:
        # Выполняется если нет аргументов
        while True:
            user_input = input('url или exit для выхода: ')
            if user_input == 'exit':
                break
            # Обновляет список селеторов из конфига
            elif user_input == 'refresh':
                parser.refresh_selectors()
                print('Селекторы обновлены')
                continue
            save_text(user_input)