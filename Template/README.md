<h1>Телеграм бот с использованием aiogram.</h1>

Этот телеграм бот позволяет настраивать торговую стратегию заказчика,
а так же подключать аккаунты в стратегию по апи ключам с биржи bybit.com



**bybit_database_connector**

Модуль создан для соединения баз данных телеграм бота с ботом, который будет
вставать в позиции на bybit.com. Собирает информацию с баз данных, возвращает 
словарь со всеми данными.



**config**

Список с главными админами, при запуске бота, админы автоматически добавляются
в базу даннух админов, если их там еще нет.
Токен телеграм бота.



**database_connector**

Классы для соединения с каждой из баз данных. Снизу модуля базы данных
инициализируются, после чего их можно импортировать в любой другой модуль.
Инициализация возможна только в одном месте, т.к. sqlite3 ругается, при 
использовании библиотеки в асинхронном aiogram.


**handlers**

Базовый модуль с хендлерами сообщений от юзеров. Ловит команды /start
/menu и каллбек с кнопки возврата в меню. В этот модуль импортируется
python-package с названием 'BUTTONS', где расположены все хандлеры и
логические цепочки каждой главной кнопки из меню.


**keyboards**

Создание инлайн клавиатур.


**hint.png**

Картинка, которая отправляется юзеру при настройках конфига бота для
его удобства.


**main**

Создание диспатчера, отсюда диспатчер импортируется в другие места.


**states**

Создание классов состояний для юзера. Классы состояний нужны для разных
логических цепочек, например для поочередного собирания данных о стратегии
или при регистрации нового юзера.


**BUTTONS**

Название модулей говорят сами за себя. Модули для управления нажатий
на кнопку от юзера.