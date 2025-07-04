# Ответы на сообщения
start_ans = 'Привет! Я FormulaNow — твой бот по Формуле 1. Я расскажу тебе, когда будет следующая гонка, кто лидирует в чемпионате и многое другое. Нажми на Меню или Кнопки, чтобы приступить к работе🏆'
next_race_ans = '*Расписание следующей гонки*\n\n'
schedule_ans = '*Расписание заездов 2025 года*\n\n'
track_ans = ''
standings_ans = '*Личный зачет 2025 года*\n_\\*если съезжает, переверни телефон_\n'
teams_ans = '*Кубок конструкторов 2025 года*\n\n'
results_ans = 'Выбери на клавиатуре, что хочешь увидеть'
last_race_ans = '*Результаты последней гонки*\n\n'
last_qualy_ans = '*Результаты последней квалификации*\n\n'
guide_ans = ''

# Шаблоны 
schedule_template = '>*{}*  *{}*   *{}*\n>    *Гонка*: {}   Квалификация: {}\n'
next_race_template = '*{name}*\n>Пятница *{fr_date}*\n>    Практика 1: {fp1_t}\n>    {fp2_n}: {fp2_t}\n\n>Суббота *{sat_date}*\n>    {fp3_n}: {fp3_t}\n>    Квалификация: {q_t}\n\n>Воскресенье *{sun_date}*\n>    *Гонка*: {r_t}'
standings_template = '>`{:2}\\. {:<27} \\- {:>3}`\n'
teams_template = '>`{:2}\\. {:<14} \\- {:>3}`\n'
track_template = '*{}*\n\n*Название трассы:* {}\n*Город:* {}\n*Длина круга:* {}\n*Число кругов:* {}\n*Число поворотов:* {}'
notification_template = '*{} состоится {}*\n{}\nНачало в *{}*\n*Не пропусти\\!*'

# Текста кнопок
next_race_button_text = 'Следующая гонка'
schedule_button_text = 'Расписание заездов'
track_button_text = 'Трасса'
standings_button_text = 'Личный зачет'
teams_button_text = 'Кубок конструкторов'
results_button_text = 'Результаты последней гонки'
last_race_button_text = 'Гонка'
last_qualy_button_text = 'Квалификация'
last_sprint_button_text = 'Спринт'
last_sprint_qualy_button_text = 'Спринт квалификация'

# Названия гран при
grand_prix_locations = [
    "🇦🇺 Австралия",
    "🇨🇳 Китай",
    "🇯🇵 Япония",
    "🇧🇭 Бахрейн",
    "🇸🇦 Саудовская Аравия",
    "🇺🇸 Майами",
    "🇮🇹 Имола",
    "🇲🇨 Монако",
    "🇪🇸 Испания",
    "🇨🇦 Канада",
    "🇦🇹 Австрия",
    "🇬🇧 Великобритания",
    "🇧🇪 Бельгия",
    "🇭🇺 Венгрия",
    "🇳🇱 Нидерланды",
    "🇮🇹 Монца",
    "🇦🇿 Азербайджан",
    "🇸🇬 Сингапур",
    "🇺🇸 Остин",
    "🇲🇽 Мехико",
    "🇧🇷 Бразилия",
    "🇺🇸 Лас\\-Вегас",
    "🇶🇦 Катар",
    "🇦🇪 Абу\\-Даби"
]

track_photoes = [
    'au',
    'ch',
    'jp',
    'bh',
    'sa',
    'ma',
    'im',
    'mc',
    'es',
    'ca',
    'at',
    'gb',
    'be',
    'hu',
    'nl',
    'mo',
    'az',
    'sg',
    'os',
    'mx',
    'br',
    'lv',
    'qa',
    'ae'
]

drivers_shortname_rus = {
    'PIA': 'О\\.Пиастри',
    'NOR': 'Л\\.Норрис',
    'VER': 'М\\.Ферстаппен',
    'RUS': 'Д\\.Расселл',
    'LEC': 'Ш\\.Леклер',
    'ANT': 'К\\.Антонелли',
    'HAM': 'Л\\.Хэмилтон',
    'ALB': 'А\\.Албон',
    'OCO': 'Э\\.Окон',
    'STR': 'Л\\.Стролл',
    'GAS': 'П\\.Гасли',
    'HUL': 'Н\\.Хюлькенберг',
    'BEA': 'О\\.Беарман',
    'HAD': 'И\\.Хаджар',
    'SAI': 'К\\.Сайнс',
    'TSU': 'Ю\\.Цунода',
    'ALO': 'Ф\\.Алонсо',
    'LAW': 'Л\\.Лоусон',
    'DOO': 'Д\\.Дуан',
    'BOR': 'Г\\.Бортолето',
    'COL': 'Ф\\.Колапинто'
}

grand_prix_dict = {
    "bahrain_2025": "🇧🇭 Бахрейн",
    "saudi_arabia_2025": "🇸🇦 Саудовская Аравия",
    "australian_2025": "🇦🇺 Австралия",
    "japanese_2025": "🇯🇵 Япония",
    "chinese_2025": "🇨🇳 Китай",
    "miami_2025": "🇺🇸 Майами",
    "emilia_romagna_2025": "🇮🇹 Имола",
    "monaco_2025": "🇲🇨 Монако",
    "spanish_2025": "🇪🇸 Испания",
    "canadian_2025": "🇨🇦 Канада",
    "austrian_2025": "🇦🇹 Австрия",
    "british_2025": "🇬🇧 Великобритания",
    "hungarian_2025": "🇭🇺 Венгрия",
    "belgian_2025": "🇧🇪 Бельгия",
    "dutch_2025": "🇳🇱 Нидерланды",
    "italian_2025": "🇮🇹 Монца",
    "azerbaijan_2025": "🇦🇿 Азербайджан",
    "singapore_2025": "🇸🇬 Сингапур",
    "united_states_2025": "🇺🇸 Остин",
    "mexican_2025": "🇲🇽 Мехико",
    "brazilian_2025": "🇧🇷 Бразилия",
    "las_vegas_2025": "🇺🇸 Лас\\-Вегас",
    "qatar_2025": "🇶🇦 Катар",
    "abu_dhabi_2025": "🇦🇪 Абу\\-Даби"
}


PARSE_DELAY = 60
