# Структура проекта
**main.py** - главный модуль.  
**config.py** - управление конфигурационным файлом.  
**config.ini** - конфигурационный файл.  
**html_parser.py** - код загрузки и обработки страницы.  
Проет содержит виртуальное окружение venv.  

# Подробней о конфигурационном файле
## Файл содержит селекторы, согласно которым будет обрабатываться страница
**selectors_blacklist** - селекторы, элементы которых будут удаляться.  
**selector_pick** - селекторы, элементы которых будут выбраны.  
**selector_for_space** - селекторы, после элементов которых будет пустая строка.  
**selectors_upper** - селекторы, текст элементов которых будет напечатан заглавными буквами.  

# Алгоритм
1. Программа получает html текст из body.
2. Удаляются элементы согласно **selectors_blacklist**(конфигурационный файл).
3. Далее происходит выбор нужных элементов при помощи selector_pick(конфигурационный файл).
4. Предварительное форматирование текста,  
    замена ссылок на "текст ссылки[ссылка]",  
    замена блочных цитат на текст в кавычках,  
    добавление пустых строк между элементами селекторов selector_for_space(конфигурационный файл),  
    замена текста элементов на заглавный, селекторы selectors_upper(конфигурационный файл).  
5. Перенос текста по словам, строка не более 80 символов, дробление слов/ссылок длиннее 80 символов.
6. Замена двух и более пустых строк, на одну.
7. Запись результата в index.txt (путь генерируется на основе URL).

# Использование
### 1. Перейти в директорию проекта
### 2. Активировать виртуальное окружение venv:
#### Windows:
```
Scripts\activate.bat
```
#### Linux:
```
.bin/activate
```
### 3. Работа программы возможна в двух режимах:
### Режим утилиты командной строки (через пробел передается аргумент url):
```
main.py [url]
```
### Интерактивный режим (при запуске main.py без аргументов)
В этом режиме возможно обновления селекторов из config.ini при помощи ввода refresh.

# Список URL, на которых происходила проверка:
https://lenta.ru/news/2020/09/03/pechernikova/  
https://lenta.ru/news/2020/09/03/secrets/  
https://lenta.ru/news/2020/09/03/us_souz/  
https://www.gazeta.ru/politics/news/2020/09/03/n_14888462.shtml  
https://www.gazeta.ru/comments/column/desnitsky/13222844.shtml  
https://www.gazeta.ru/science/news/2020/09/03/n_14887748.shtml  
https://meduza.io/feature/2020/09/03/ne-znaesh-mery-poydesh-na-nary  
https://meduza.io/feature/2020/09/02/snachala-vypit-kofe-potom-pogladit-kota-kogda-tut-voobsche-rabotat  
https://meduza.io/feature/2020/09/03/nikakie-obvineniya-my-ne-sklonny-vosprinimat-kreml-ob-otravlenii-berlinskogo-patsienta-alekseya-navalnogo  
https://meduza.io/feature/2020/09/03/chelovecheskiy-golos-pedro-almodovara-film-o-zamknutosti-i-osvobozhdenii-rezhisser-snyal-ego-posle-togo-kak-perenes-kovid  
https://habr.com/ru/company/ruvds/blog/517638/  
https://habr.com/ru/post/517888/  
https://72.ru/text/animals/69457061/  
https://ria.ru/20200905/samolet-1576825317.html  
## Результат проверки находится в сгенерированных директориях.  

# Дальнейшее развитие
Изучение строения статей интересующих сайтов, добавление новых селекторов в конфигурационный файл.
