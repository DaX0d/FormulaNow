PARSE_DELAY = 300
CURRENT_YEAR = 2026

DATE_FORMAT = '%d.%m'
TIME_FORMAT = '%H:%M'

# Ответы на сообщения
start_ans = 'Привет! Я FormulaNow — твой бот по Формуле 1. Я расскажу тебе, когда будет следующая гонка, кто лидирует в чемпионате и многое другое. Нажми на Меню или Кнопки, чтобы приступить к работе🏆'
next_race_ans = '*Расписание следующей гонки*\n\n'
schedule_ans = f'*Расписание заездов {CURRENT_YEAR} года*\n\n'
track_ans = ''
standings_ans = f'*Личный зачет {CURRENT_YEAR} года*\n_\\*если съезжает, переверни телефон_\n'
teams_ans = f'*Кубок конструкторов {CURRENT_YEAR} года*\n\n'
results_ans = 'Выбери на клавиатуре, что хочешь увидеть'
last_race_ans = '*Результаты последней гонки*\n\n'
last_qualy_ans = '*Результаты последней квалификации*\n\n'
last_sprint_ans = '*Результаты последнего спринта*\n\n'
last_sprint_qualy_ans = '*Результаты последней спринт квалификации*\n\n'
guide_ans = ''

# Шаблоны 
schedule_template = '>*{}*  *{}*   *{}*\n>    *Гонка*: {}   Квалификация: {}\n'
next_race_template = '*{name}*\n>Пятница *{fr_date}*\n>    Практика 1: {fp1_t}\n>    {fp2_n}: {fp2_t}\n\n>Суббота *{sat_date}*\n>    {fp3_n}: {fp3_t}\n>    Квалификация: {q_t}\n\n>Воскресенье *{sun_date}*\n>    *Гонка*: {r_t}'
standings_template = '>`{:27} \\- {:>3}`\n'
teams_template = '>`{:2}\\. {:<17} \\- {:>3}`\n'
track_template = '*{}*\n\n*Название трассы:* {}\n*Город:* {}\n*Длина круга:* {}\n*Число кругов:* {}\n*Число поворотов:* {}'
notification_template = '*{} состоится {}*\n{}\nНачало в *{}*\n*Не пропусти\\!*'
race_week_notification_template = '*RACE WEEK*\n*{}*'

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
list_of_users_button_text = 'Список пользователей'
number_of_users_button_text = 'Количество пользователей'
parser_data_button_text = 'Данные парсера'
parser_reload_button_text = 'Перезапуск парсера'
notifications_reload_button_text = 'Перезапуск уведомлений'

# Названия гран при
schedule_locations_translation = {
    "Australia": "🇦🇺 Австралия",
    "China": "🇨🇳 Китай",
    "Japan": "🇯🇵 Япония",
    "Bahrain": "🇧🇭 Бахрейн",
    "Saudi Arabia": "🇸🇦 Саудовская Аравия",
    "Miami Gardens": "🇺🇸 Майами",
    "Canada": "🇨🇦 Канада",
    "Monaco": "🇲🇨 Монако",
    "Barcelona": "🇪🇸 Барселона",
    "Austria": "🇦🇹 Австрия",
    "United Kingdom": "🇬🇧 Великобритания",
    "Belgium": "🇧🇪 Бельгия",
    "Hungary": "🇭🇺 Венгрия",
    "Netherlands": "🇳🇱 Нидерланды",
    "Italy": "🇮🇹 Монца",
    "Madrid": "🇪🇸 Мадрид",
    "Azerbaijan": "🇦🇿 Азербайджан",
    "Singapore": "🇸🇬 Сингапур",
    "Austin": "🇺🇸 Остин",
    "Mexico": "🇲🇽 Мексика",
    "Brazil": "🇧🇷 Бразилия",
    "Las Vegas": "🇺🇸 Лас-Вегас",
    "Qatar": "🇶🇦 Катар",
    "United Arab Emirates": "🇦🇪 Абу-Даби"
}

tracks = {
    "Australia": "australia.png",
    "China": "china.png",
    "Japan": "japan.png",
    "Bahrain": "bahrain.png",
    "Saudi Arabia": "jeddah.png",
    "Miami Gardens": "miami.png",
    "Canada": "canada.png",
    "Monaco": "monaco.png",
    "Barcelona": "barcelona.png",
    "Austria": "austria.png",
    "United Kingdom": "silverstone.png",
    "Belgium": "spa.png",
    "Hungary": "hungary.png",
    "Netherlands": "zandvoort.png",
    "Italy": "monza.png",
    "Madrid": "madrid.png",
    "Azerbaijan": "baku.png",
    "Singapore": "singapore.png",
    "Austin": "austin.png",
    "Mexico": "mexico.png",
    "Brazil": "brazil.png",
    "Las Vegas": "las_vegas.png",
    "Qatar": "qatar.png",
    "United Arab Emirates": "abu_dhabi.png"
}

session_name_translation = {
    'Practice 1': 'Практика 1',
    'Practice 2': 'Практика 2',
    'Practice 3': 'Практика 3',
    'Sprint Qualifying': 'Квалификация к спринту',
    'Sprint': 'Спринт',
    'Qualifying': 'Квалификация',
    'Race': 'Гонка'
}

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

driver_translation = {
    "albon": "А.Албон",
    "alonso": "Ф.Алонсо",
    "antonelli": "К.Антонелли",
    "bearman": "О.Берман",
    "bortoleto": "Г.Бортолето",
    "bottas": "В.Боттас",
    "colapinto": "Ф.Колапинто",
    "gasly": "П.Гасли",
    "hadjar": "И.Хаджар",
    "hamilton": "Л.Хэмилтон",
    "hulkenberg": "Н.Хюлькенберг",
    "lawson": "Л.Лоусон",
    "leclerc": "Ш.Леклер",
    "arvid_lindblad": "А.Линдблад",
    "norris": "Л.Норрис",
    "ocon": "Э.Окон",
    "piastri": "О.Пиастри",
    "perez": "С.Перес",
    "russell": "Д.Расселл",
    "sainz": "К.Сайнс",
    "stroll": "Л.Стролл",
    "max_verstappen": "М.Ферстаппен",
    "tsunoda": "Ю.Цунода",
    "doohan": "Д.Дуан"
}

drivers_shortname_rus = {
    'PIA': 'О.Пиастри',
    'NOR': 'Л.Норрис',
    'VER': 'М.Ферстаппен',
    'RUS': 'Д.Расселл',
    'LEC': 'Ш.Леклер',
    'ANT': 'К.Антонелли',
    'HAM': 'Л.Хэмилтон',
    'ALB': 'А.Албон',
    'OCO': 'Э.Окон',
    'STR': 'Л.Стролл',
    'GAS': 'П.Гасли',
    'HUL': 'Н.Хюлькенберг',
    'BEA': 'О.Беарман',
    'HAD': 'И.Хаджар',
    'SAI': 'К.Сайнс',
    'TSU': 'Ю.Цунода',
    'ALO': 'Ф.Алонсо',
    'LAW': 'Л.Лоусон',
    'DOO': 'Д.Дуан',
    'BOR': 'Г.Бортолето',
    'COL': 'Ф.Колапинто',
    "LIN": "А.Линдблад",
    "BOT": "В.Боттас",
    "PER": "С.Перес",
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

teams_names_dict = {
    'mclaren': 'McLaren',
    'red_bull': 'Red Bull',
    'ferrari': 'Ferrari',
    'mercedes': 'Mercedes',
    'williams': 'Williams',
    'haas': 'Haas',
    'rb': 'RB',
    'aston_martin': 'Aston Martin',
    'alpine': 'Alpine',
    'sauber': 'Sauber'
}
