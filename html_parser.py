from bs4 import BeautifulSoup
from config import Config
import requests
import re


class Parser():
    def __init__(self):
        self.config = Config('config.ini')
        self.SELECTORS_BLACKLIST = eval(
            self.config.get_value('Parser', 'selectors_blacklist'))
        self.SELECTOR_PICK = self.config.get_value('Parser', 'selector_pick')
        self.SELECTOR_FOR_SPACE = eval(
            self.config.get_value('Parser', 'selector_for_space'))
        self.SELECTOR_UPPER = eval(
            self.config.get_value('Parser', 'selectors_upper'))

    def get_body_text(self, url):
        '''Возвращает строку, содержащую тег body из url'''
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')

            return str(soup.select('body'))
        except:
            return 'Не удалось скачать страницу'

    def del_tags(self, html, selector):
        '''
        Удаляет все элементы по selector(строка) из строки html,
        возвращает измененную строку html
        '''
        soup = BeautifulSoup(html, 'lxml')

        while True:
            items = soup.select_one(selector)
            if items:
                items.decompose()
            else:
                break

        return str(soup)

    def clear_html(self, html, selectors):
        '''
        Удаляет все элементы из кортежа строк selectors из строки html, 
        возвращает измененную строку html
        '''
        for selector in selectors:
            html = self.del_tags(html, selector)

        return html

    def select_need_block(self, html, selector):
        '''Выбирает элементы согласно selector(строка), возвращает строку'''
        soup = BeautifulSoup(html, 'lxml')
        selected = soup.select(selector)
        output_string = ''
        # Склеивание выбранных элементов
        for elem in selected:
            # Проверка на дублирование элементов
            if str(elem) not in output_string:
                output_string += str(elem)

        return output_string

    def preformat_text(self, html):
        '''Форматирует текст из строки html, возвращает строку'''
        soup = BeautifulSoup(html, 'lxml')

        # Форматирование ссылок
        while soup.select_one('a'):
            try:
                tag = soup.select_one('a')
                str_replace = tag.text + '[{}]'.format(tag['href'])
                tag.replace_with(str_replace)
            except:
                tag.replace_with('')

        # Форматирование блочных цитат
        while soup.select_one('blockquote'):
            try:
                tag = soup.select_one('blockquote')
                str_replace = '"{}"\n\n'.format(tag.text)
                tag.replace_with(str_replace)
            except:
                tag.replace_with('')

        # Добавление пустых строк между селекторами из SELECTOR_FOR_SPACE
        for selector in self.SELECTOR_FOR_SPACE:
            while soup.select_one(selector):
                tag = soup.select_one(selector)
                # Если селектор в SELECTOR_UPPER, делает текст заглавным
                if selector in self.SELECTOR_UPPER:
                    str_replace = tag.text.upper() + '\n\n'
                else:
                    str_replace = tag.text + '\n\n'
                tag.replace_with(str_replace)

        return soup.text

    def del_duplicate_newstr(self, text):
        '''
        Принимает строку text, 
        возвращает строку с не более чем двумя переносами подряд
        '''
        result = re.findall(r'\n{3,}', text)

        for item in result:
            text = text.replace(item, '\n\n')

        return text

    def wrap_text(self, text):
        '''
        Принимает строку, 
        возвращает форматированную строку (перенос по словам)
        '''
        max_len = 80
        text = text.split('\n\n')
        output_text = ''
        for paragraph in text:
            paragraph = paragraph.split()
            buf_str = ''
            for word in paragraph:
                # Если слово длинее макс длины строки, разбивает его
                if len(word) + len(buf_str) + 2 > max_len:
                    if len(word) > max_len:
                        start = 0
                        buf_str += '\n'
                        for char in word:
                            buf_str += char
                            start += 1
                            if start % 80 == 0:
                                buf_str += '\n'
                    else:
                        output_text += buf_str + '\n'
                        buf_str = word + ' '
                else:
                    buf_str += word + ' '
            output_text += buf_str + '\n\n'

        return output_text.strip()

    def get_text_url(self, url):
        '''
        Принимает строку url, 
        возвращает "полезный" текст с предварительным форматированием
        '''
        html = self.get_body_text(url)
        html = self.clear_html(html, self.SELECTORS_BLACKLIST)
        html = self.select_need_block(html, self.SELECTOR_PICK)
        html = self.preformat_text(html)
        html = self.wrap_text(html)
        html = self.del_duplicate_newstr(html)

        return html

    def refresh_selectors(self):
        '''Загружает новые данные из файла конфигурации'''
        self.config = Config('config.ini')
        self.SELECTORS_BLACKLIST = eval(
            self.config.get_value('Parser', 'selectors_blacklist'))
        self.SELECTOR_PICK = self.config.get_value('Parser', 'selector_pick')
        self.SELECTOR_FOR_SPACE = eval(
            self.config.get_value('Parser', 'selector_for_space'))
        self.SELECTOR_UPPER = eval(
            self.config.get_value('Parser', 'selectors_upper'))