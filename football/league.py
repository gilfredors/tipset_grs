

def get_list_relevant_countries():
    return [
        'World', 'England', 'France', 'Brazil', 'Germany', 'Netherlands',
        'Portugal', 'Norway', 'Poland', 'Sweden',
        'Denmark', 'Argentina', 'Italy', 'Spain', 'Belgium',
        'Turkey', 'Switzerland', 'Austria', 'Russia', 'Scotland'
    ]


def get_dict_followed_country_and_competition():
    country_and_competitions = {
        "Argentina": [
            "Primera Division",
            "Copa Argentina",
            "Copa de la Superliga",
            "Trofeo de Campeones de la Superliga",
        ],
        "Austria": [
            "Tipp3 Bundesliga",
            "Cup",
        ],
        "Belgium": [
            "Jupiler Pro League",
            # "Cup",
            "Super Cup",
        ],
        "Brazil": [
            "Serie A",
            "Copa Do Brasil",
            "Supercopa do Brasil",
        ],
        "Denmark": [
            "Superligaen",
            "DBU Pokalen",
        ],
        "England": [
            "Premier League",
            "Championship",
            "FA Cup",
            "League Cup",
            "Community Shield",
        ],
        "France": [
            "Ligue 1",
            "Coupe de la Ligue",
            "Coupe de France",
        ],
        "Germany": [
            "Bundesliga 1",
            "DFB Pokal",
            "Super Cup",
        ],
        "Italy": [
            "Serie A",
            "Coppa Italia",
            "Super Cup",
        ],
        "Netherlands": [
            "Eredivisie",
            "Super Cup",
        ],
        "Norway": [
            "Eliteserien",
            "NM Cupen",
            "Super Cup",
        ],
        "Poland": [
            "Ekstraklasa",
            "Cup",
        ],
        "Portugal": [
            "Primeira Liga",
            "Super Cup",
        ],
        "Russia": [
            "Premier League",
            "Cup",
            "Super Cup",
        ],
        "Scotland": [
            "Premiership",
            "FA Cup",
        ],
        "Spain": [
            "Primera Division",
            "Copa del Rey",
            "Super Cup",
        ],
        "Sweden": [
            "Allsvenskan",
            "Superettan",
            "Svenska Cupen",
        ],
        "Switzerland": [
            "Super League",
            "Schweizer Pokal",
        ],
        "Turkey": [
            "Super Lig",
            "Cup",
            "Super Cup",
        ],
        "World": [
            "World Cup",
            "UEFA Champions League",
            "UEFA Europa League",
            "Euro Championship",
            "UEFA Nations League",
            "Africa Cup of Nations",
            "Asian Cup",
            "Copa America",
            "Friendlies",
            "CONMEBOL Sudamericana",
            "CONMEBOL Libertadores",
            "FIFA Club World Cup",
            "Confederations Cup",
            "CONCACAF Gold Cup",
            "World Cup - Qualification Africa",
            "World Cup - Qualification Asia",
            "World Cup - Qualification CONCACAF",
            "World Cup - Qualification Europe",
            "World Cup - Qualification Oceania",
            "World Cup - Qualification South America",
            "Asian Cup - Qualification",
            "Africa Cup of Nations - Qualification",
        ]}

    return country_and_competitions
