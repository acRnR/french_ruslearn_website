 *Электронный тренажер для студентов, изучающих русский язык как иностранный. Train Tool for French Students*
-------------------------------------------------------------------------------------------------------------

сайт временно работает по адресу http://traintoolforfrenchstudents.pythonanywhere.com/

Дополнительные предустановки
----------------------------

Установить в виртуальное окружение:
- flask
- flask-SQLAlchemy
- flask-security

Создать файл conf.py и задать там две переменные - электронную почту, с которой должны отправляться письма новым зарегистрированным пользователям и пароль от неё:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MAILUN = 'ЭЛЕКТРОННАЯ ПОЧТА'
PASSWORD = 'ПАРОЛЬ'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Описание работы программы сайта-тренажёра (french_rafl_learners.py)
-------------------------------------------------------------------

Код программы для удобства разделён на 9 секций

**1. Импорт необходимых файлов, модулей, расширений и их частей**

**2. Настройки конфигураций и создание связи с базой данных пользователей**

**3. Функции, получающие данные для выведения на страницах сайта**

функция | что делает | входные данные | возвращает
------- | ---------- | -------------- | ----------
distance(a, b) | считает расстояние Левенштейна между введенным словом и правильным ответом | a и b - сравниваемые слова| расстояние
call_db(tbl) | посылает запрос в базу данных со словами voc.db | tbl - таблица, данные которой мы хотим получить | словарь с данными таблицы
usermailget | получает логин(почту) текущего пользователя |   | адрес электронной почты
voc_maker(ps, categories) | собирают слова для отображения на страницах с темами/частями речи| ps - часть речи, categories - массив из названий категорий слов, которые должны быть в той или иной секции словаря | словарь вида {*категория*: [["слово", "перевод"],["слово", "перевод"]]}
sorting, sorting_back, gramm_sorting | собирают слова для квизов и упражнений | ps - часть речи, categories - массив из названий категорий слов, f - дополнительная функция создания контекста, n - для отличения составления большого квиза/упражнения от маленького | словарь, готовый к созданию теста
ex_genpl_maker, prs_conj_maker | создают контекст для вопросов на грамматику | | словарь с контекстами, готовый к обработке функцией gramm_sorting
big q_maker, quiz_maker | Создают тесты | часть речи, категории слов, функции, которые структурируют информацию для вопросов | словарь вида {номервопроса: [вопрос, ответ], номервопроса: [вопрос, ответ]}

**4. Заглавная страница и страница клавиатуры**

Вкладка клавиатуры открывается, если нажать на иконку клавиатуры в квизе/упражнении, предполагающем введение ответа на русском языке. Работа клавиатуры при нажатии на клавиши осуществляется файлами keyboard_key.js и keyboard_all.js.

**5. Страницы с маленькими квизами (тестами на оценку)**

Квизы состоят из 5 вопросов по заданной категории слов. В случае если пользователь пытается отправить незаполненную форму, всплывает уведомление с просьбой заполнить поле. Если пользователь ввел полностью правильный ответ, он получает 1 балл за вопрос, если допущена одна ошибка (расстояние Левенштейна = 1) - полбалла, если ошибок больше - 0 баллов. В конце прохождения теста пользователь попадает на страницу с результатами: Выводится колличество баллов за тест и все вопросы с правильными ответами для всех заданий, которые пользователь решил неверно.

**6. Страницы с большими квизами**

Квизы состоят из 20 вопросов по всем (или половине, в случае тестов из функций bigconj(v1) и bigconj(v2)) категориям заданной части речи. В случае если пользователь пытается отправить незаполненную форму, всплывает уведомление с просьбой заполнить поле. Если пользователь ввел полностью правильный ответ, он получает 1 балл за вопрос, если допущена одна ошибка (расстояние Левенштейна = 1) - полбалла, если ошибок больше - 0 баллов. В конце прохождения теста пользователь попадает на страницу с результатами: Выводится колличество баллов за тест и все вопросы с правильными ответами для всех заданий, которые пользователь решил неверно.

**7. Страницы с маленькими упражнениями (тестами не на оценку)**

Упражнения состоят из 5 вопросов по заданной категории слов. В случае если пользователь пытается отправить незаполненную форму, всплывает уведомление с просьбой заполнить поле; если вводится неверный ответ, всплывает уведомление с верным ответом, пользователю предлагается снова его ввести.

**8. Страницы с большими упражнениями**

Упражнения состоят из 20 вопросов по всем (или половине, в случае тестов из функций bigconj(v1) и bigconj(v2)) категориям заданной части речи. В случае если пользователь пытается отправить незаполненную форму, всплывает уведомление с просьбой заполнить поле; если вводится неверный ответ, всплывает уведомление с верным ответом, пользователю предлагается снова его ввести.

**9. Страницы с материалами по каждой теме/части речи**

При переходе на такую страницу программа собирает все тесты на часть речи, которой посвящена страница, в глобальный словарь sess_2.

База данных voc.db
------------------

Таблица | Столбец | Назначение столбца | Возможные значения
------- | ------- | ------------------ | ------------------
rus_words | id | primary key |
rus_words | search | лемма без ударения, для удобства поиска по базе |
rus_words | Rus | лемма с ударением |
rus_words | Fran | перевод русского слова |
rus_words | part_of_speech | часть речи слова | s (сущ), v (глаг), adv (нареч), phr (устойчивые словосочетания/идиомы)
rus_words | category| категория слова| 1d, m, n, 3d, indecl - типы склонения; pl_tantum; 1_productif, 1_sans_diff, 1_avec_diff, 1_base_altern, 2_productif, 2_improductif - типы склонения; adv;
rus_words | gen | род (столбец заполняется только для существительных) | f, m, n, cmn (общий род), 0 (для pluralia tantum)
rus_words | extra info | столбец для записи дополнительной, важной для заданий информации о слове | sg_tantum
s_decl | id | primary key | 
s_decl | search_id | foreign key - id слова из таблицы rus_words |
s_decl | nom_sg, gen_sg, dat_sg, acc_sg, instr_sg, abl_sg, nom_pl, gen_pl, dat_pl, acc_pl, instr_pl, abl_pl | формы падежей и чисел существительных | форма слова с проставленным ударением
v_conj | id | primary key | 
v_conj | search_id | foreign key - id слова из таблицы rus_words |
v_conj | prs1sg, prs2sg, prs3sg, prs1pl, prs2pl, prs3pl | формы лиц и чисел настоящего/будущего времени глаголов | форма с проставленным ударением

Прочие замечания
----------------

- Было решено по большей части для хранения данных внутри сессии использовать отдельный глобальный словарь sess_2, а не встроенный словарь cookies flask.session, потому что sessions не справляется с таким большим объемом данных, который нам нужно хранить (cookies вообще для этого не предназначены).
- Размер тестов (количество вопросов в одном тесте) можно поменять в функциях big q_maker и quiz_maker
