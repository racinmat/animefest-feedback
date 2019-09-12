import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import partial
import seaborn as sns
import requests

info_suffix = ' [Dozvěděl(a) jsem se zajímavé informace]'
fun_suffix = ' [Bavil(a) jsem se]'

categories = {
    'soutěže': [ 
        'Animekvíz', 'Cosplay debut', 'Cosplay soutěž', 'Cosplay video', 'Festdance', 'Soutěžní AMV', 'Vyhlášení výsledků', 
    ], 
    'přednášky': [
        '12 ran cosplayerových', '2. světová válka z pohledu Japonska a život císaře Hirohita', '3D tisk v cosplayi: Od modelování po barvení', 'Alternativní móda: Od ponožky po klobouk', 'An Introduction to Leather Crafting', 
        'Anime světy, ve kterých (ne)chcete žít', 'BJD od Ludvíka XIV. až po BTS', 'Bojuj podle svého charakteru', 'Cosplay and Otaku History in Japan', 'Cosplay armor: From reference to wearable costume', 
        'Crossdressing - the hell is dat?', 'Designing Male Characters Fanservice: The Struggle', 'Do Japonska za idoly', 'Doll Photography', 'Fake Is Sad/Bootleg Panel', 'Filmoví skladatelé Japonska č. 2', 
        'Gača hry aneb Lootboxy na asijský způsob', 'Gejša: Tajemství za stěnami čajovny', 'Ghibli známé neznámé', 'Godzilla, just a rubber monster, right?', 'Gothic – hudba, móda, subkultura', 
        'Historická přesnost zbrojí v anime na vybraných příkladech', 'Indonésie – země ohně', 'Jak na anime make-up', 'Jak na psaní – Od teorie k praxi', 'Jak se připravit na cosplay focení', 'Jak sehnat (nejen) jaoi v totalitním státu', 
        'Jak si plnit sny pomocí anime', 'Japanacorps, WTF?!', 'Japonský rok v emodži', 'Letem jiným světem', 'Lolitou každý den', 'Líčení pro trdla od trdla', 'Madoka Magica a ti druzí, co selhali', 'Manga novinky u nás!', 
        'Manga pro dospívající dívky: Co na ní milujeme a nesnášíme', 'Maul Cosplay Q&A', 'My Hero Academy', 'Módní přehlídka 101', 'Nebojte se zahraničních soutěží!', 'Nový kreslíř na scéně: umělá inteligence!', 
        'Očekávání vs. realita: Člověk 2.0, mecha a vesmírné lodě', 'Pen & Paper role-playing hry', 'Proč (ne)jet do Jižní Koreje', 'Receptář tetičky Mitsu nejen pro začínající lolity', 'Remaky anime', 'Reputace & renesance D&D', 
        'Resident Evil – Od zrození po současnost', 'Rámen po česku', 'Sekiro, Nioh a ti další…', 'Slasti a strasti japonského randění', 'Slavnostní zahájení + křest Vějíře', 'Stereotyp – NÁMITKA!', 'Svět japonských idolů', 
        'Taková normální japonská rodinka', 'Viktoriánské úpravy vlasů', 'World cosplay panel', 'Zakončení conu', 'Zákeřné vody videoherního pirátství', 
    ], 
    'workshopy': [
        'Aikido Ikigai Dojo Brno', 'Aikikai Aikido Brno', 'Boj dýkou a nožem', 'Boj tesákem', 'Choker', 'Cosplay Act Workshop', 'Yoshinkan aikido', 'Kaligrafie', 'Kendo', 'Kensei Dojo Brno', 'Kimono workshop', 'Sraz AMV', 
        'Háčkování plyšových zvířátek', 'I pád je posun vpřed', 'Jak se při cosplayi neztrapnit se zbraní', 'Jo, bokken, tanto aneb Obrana proti japonským zbraním', 'Květiny Ikebana', 'Mák a jeho klacek aneb I monk si s holí leccos dovolí', 
        'Náušnice ze skleněných kapek', 'Od základů po pokročilejší retuše nejen cosplay fotografie', 'Omalovánky', 'Origami Workshop', 'Rozcvička pro družinku aneb Dračí doupě po ránu', 'Rytíř, meč a štít aneb Líný šerm', 
        'Růže ze saténových stužek', 'Sebeobrana nejen pro dámy', 'Sebeobrana po japonsku', 'Taneční k-pop workshop', 'Vyšívání', 'Válečník mazlivě obouručákem tě mlaskne', 'Výroba vlastního diáře/skicáku', 
        'Workshop animace v Clip Studio Paint', 'Základy svícení s profesionálními záblesky a jejich modifikátory'
    ], 
    'promítání': [
        '3D holka', 'A to je špatně, když se chodím seznamovat do kobek? Orionův šíp', 'Bůh žehnej tomuto nádhernému světu', 'Fashion Mix', 'Gamers!', 'Já malý čarodějka', 'Květina zaslíbená rannímu loučení', 'Lolita Music Mix: Novinky', 
        'Mirai, dívka z budoucnosti', 'Módní kolekce 2019', 'Noc je krátká, tak kráčej dál, děvče', 'Penguin Highway', 'Pohodářky', 'ReLIFE', 'Symfonie z jiného světa', 'Tipy pro život mimo realitu', 'Vzestup hrdiny štítu', 
        'Zombie Land Saga', 
    ],
    'doplňkový program': [
        'AMV Budíček', 'AMV Mortal Combat', 'AMV Nočník', 'AMV Večerníček', 'BTS Army sraz', 'Vějíř – autogramiáda a beseda', 'Anime novinky očima protřelých fanoušků', 'Budoucnost českých anime conů', 
        'K-pop – random dance CZHW', 'Sčítání žije!', 'Turnaj v šermu Aréna Alerie', 'Dračí doupě', 
    ],
    'divadlo': ['Festovní koncert', 'Kamui – The Samurai Sword Artists', 'Lolita Fashion Show', 'Malé divadlo kjógenu', ],
    }

col_to_category = {col: category for category, cols in categories.items() for col in cols}

def get_names_to_replace():
    return {
    'BJD od Ludvíka XIV. až po BTS ': 'BJD od Ludvíka XIV. až po BTS', 
    'Gejša: Tajemství za stěnami čajovny ': 'Gejša: Tajemství za stěnami čajovny', 
    'Jak sehnat (nejen) jaoi v totalitním státu ': 'Jak sehnat (nejen) jaoi v totalitním státu',
    'Líčení pro trdla od trdla ': 'Líčení pro trdla od trdla', 'World Cosplay Panel': 'World cosplay panel',
    'Výroba vlastního diáře/skicáku ': 'Výroba vlastního diáře/skicáku', 
    'I pád je posun vpřed – workshop': 'I pád je posun vpřed', 'Sebeobrana po japonsku – workshop': 'Sebeobrana po japonsku',
    'Kendo – vystoupení/workshop': 'Kendo', 'Aikido Ikigai Dojo Brno – vystoupení/workshop': 'Aikido Ikigai Dojo Brno',
    'Aikikai Aikido Brno – vystoupení/workshop': 'Aikikai Aikido Brno', 'Yoshinkan aikido – vystoupení/workshop': 'Yoshinkan aikido',
    'Kensei Dojo Brno - vystoupení/workshop': 'Kensei Dojo Brno', 'Turnaj 1. kolo': 'Turnaj v šermu Aréna Alerie', 
    'Turnaj 2. kolo': 'Turnaj v šermu Aréna Alerie', 'Turnaj 3. kolo': 'Turnaj v šermu Aréna Alerie', 
    'Turnaj Finále': 'Turnaj v šermu Aréna Alerie',
    }

def load_form_data():
    df_form = pd.read_excel('Feedback_Animefest_2019.xlsx', sheet_name='Form Responses 1')
    df_form['Timestamp'] = pd.to_datetime(df_form['Timestamp'])
    
    df_form = df_form.replace(to_replace={
        '😐v pohodě': 'v pohodě', '😃dobré': 'dobré', '😞špatné': 'špatné', '😐 v pohodě': 'v pohodě', '😃 dobré': 'dobré', 
        '😞 špatné': 'špatné', '😃Ano': 'Ano', '😞Ne': 'Ne'})
    
    # several columns with same name, mutually exlusively filled, merging those
    duplicit_columns = [i for i in df_form.columns if i.endswith('.1')]
    for i in duplicit_columns:
        assert df_form[[i[:-2], i]].notnull().sum(axis=1).max() == 1  # only one column is filled, the other is N/A
        df_form.loc[df_form[i].notnull(), i[:-2]] = df_form[df_form[i].notnull()][i]
    df_form = df_form.drop(columns=duplicit_columns)
    
    # renaming columns with additional space
    program_cols_to_strip_space = ['Aikido Ikigai Dojo Brno', 'Aikikai Aikido Brno', 'Kensei Dojo Brno']
    replace_dict = {}
    for col in program_cols_to_strip_space:
        replace_dict[f'{col} {info_suffix}'] = f'{col}{info_suffix}'
        replace_dict[f'{col} {fun_suffix}'] = f'{col}{fun_suffix}'
        replace_dict[f'Komentář: {col} '] = f'Komentář: {col}'
    df_form = df_form.rename(columns=replace_dict)
    
    # replacing annoyingly long answer
    df_form = df_form.replace({'chci hodnotit podrobně (je toho opravdu hodně, čím víc vyplníte, tím vděčnější budeme)': 
                               'chci hodnotit podrobně'})
    
    columns_series = df_form.columns.to_series()
    program_columns_ratings = columns_series[columns_series.str.contains(info_suffix, regex=False) | columns_series.str.contains(fun_suffix, regex=False)]
    
    program_columns = pd.Series(program_columns_ratings.str.replace(info_suffix, '', regex=False).str.replace(fun_suffix, '', regex=False).unique())

    # some columns that should have same content have nans somewhere, fixing this
    # if one column marks not attended, and second is null, value is inferred
    not_attended_arr = ['Nedostal(a) jsem se', 'Nezúčastnil(a) jsem se']
    for i in program_columns:
        info_cond = df_form[i+info_suffix].isna() & df_form[i+fun_suffix].isin(not_attended_arr)
        fun_cond = df_form[i+fun_suffix].isna() & df_form[i+info_suffix].isin(not_attended_arr)
        df_form.loc[info_cond, i+info_suffix] = df_form[info_cond][i+fun_suffix]
        df_form.loc[fun_cond, i+fun_suffix] = df_form[fun_cond][i+info_suffix]

    # if one column marks not attended, and second is rating, not attended is set to null
    for i in program_columns:
        info_cond = df_form[i+fun_suffix].isin(['dobré', 'v pohodě', 'špatné']) & df_form[i+info_suffix].isin(not_attended_arr)
        fun_cond = df_form[i+info_suffix].isin(['dobré', 'v pohodě', 'špatné']) & df_form[i+fun_suffix].isin(not_attended_arr)
        df_form.loc[info_cond, i+info_suffix] = np.nan
        df_form.loc[fun_cond, i+fun_suffix] = np.nan

    # some columns that should have same type of attendence have different. Converting 'Nedostal(a) jsem se' to 'Nezúčastnil(a) jsem se'
    for i in program_columns:
        info_cond = (df_form[i+info_suffix] == 'Nedostal(a) jsem se') & (df_form[i+fun_suffix] == 'Nezúčastnil(a) jsem se')
        fun_cond = (df_form[i+fun_suffix] == 'Nedostal(a) jsem se') & (df_form[i+info_suffix] == 'Nezúčastnil(a) jsem se')
        df_form.loc[info_cond, i+info_suffix] = df_form[info_cond][i+fun_suffix]
        df_form.loc[fun_cond, i+fun_suffix] = df_form[fun_cond][i+info_suffix]
    
    # merging same questions named differently for detailed and not detailed version
    columns_to_merge = {'Úvodní a závěrečné video': 'Úvodní/závěrečné video', 
                    'Připadá vám téma důležité pro zážitek na conu?': 'Připadá vám AF téma pro zážitek na conu důležité?', 
                    'Komentář: Připadá vám téma důležité pro zážitek na conu': 'Komentář: Připadá vám téma pro zážitek na conu důležité?',
                    'Komentář: Letošní téma a frakce:': 'Komentář: Letošní téma a frakce',
                    'Co se vám na aplikaci líbilo, v čem vám pomohla?': 
                        'Co se vám na aplikaci líbilo? Co chcete do příště změnit nebo doplnit?'
                   }

    for col_from, col_to in columns_to_merge.items():
        assert df_form[[col_from, col_to]].notnull().sum(axis=1).max() == 1  # only one column is filled, the other is N/A
        df_form.loc[df_form[col_from].notnull(), col_to] = df_form[df_form[col_from].notnull()][col_from]
    df_form = df_form.drop(columns=columns_to_merge.keys())

    # cleaning open questions by replacing nan by empty string
    open_answers = [i for i in df_form.columns if len(df_form[i].unique()) > 20 or 'Komentář:' in i] + ['Poznámky k doprovodnému programu']
    for col in open_answers:
        df_form[col] = df_form[col].fillna('')
    
    # preparing aggregations
    form_ratings = df_form[program_columns_ratings].apply(lambda x: x.value_counts(), axis=0)
    attended_col = form_ratings.loc[['dobré', 'v pohodě', 'špatné']].fillna(0).sum(axis=0).rename('Zúčastnil(a) jsem se')
    form_attends = pd.concat((attended_col, form_ratings.loc['Nedostal(a) jsem se']), axis=1)

    form_ratings = form_ratings.drop('Nezúčastnil(a) jsem se')
    
    return df_form, columns_series, program_columns_ratings, program_columns, form_ratings, form_attends, open_answers

def load_app_data():
    df_app = pd.read_excel('Feedback_Animefest_2019.xlsx', sheet_name='Appky')
    df_app['čas feedbacku'] = pd.to_datetime(df_app['čas feedbacku'])
    
    # fixing non-aligned names
    for name_from, name_to in get_names_to_replace().items():
        df_app.loc[df_app['název'] == name_from, 'název'] = name_to

    # cleaning data, keeping only last rating
    df_app['user_program'] = df_app['uživatel'] + ' ' + df_app['program ID'].astype(str)
    df_app = df_app.groupby(['user_program']).apply(lambda x: x.sort_values(by='čas feedbacku', ascending=False).head(1))
    
    return df_app

def load_api_info(df_form_columns):
    schedule_entries = requests.get('https://www.animefest.cz/api/v1/schedule/entries/2/cs').json()
    df_schedule = pd.DataFrame(schedule_entries['entries'])
    df_schedule = df_schedule.set_index('scheduleEntryId')
    
    timetable_entries = requests.get('https://www.animefest.cz/api/v1/schedule/timetable/2/cs').json()
    df_timetable = pd.DataFrame(timetable_entries['timetable'])
    df_timetable = df_timetable.set_index('scheduleShowingId')
    df_timetable['from'] = pd.to_datetime(df_timetable['from'])
    df_timetable['to'] = pd.to_datetime(df_timetable['to'])
    
    locs_entries = requests.get('https://www.animefest.cz/api/v1/schedule/locations/2/cs').json()
    df_locs = pd.DataFrame(locs_entries['locations'])
    df_locs = df_locs.set_index('locationId')
    df_locs['capacity'] = 0
    
    capacities = {
        'Rotunda': 500, 'A2, hlavní pódium': 450, 'A2, studio stage': 330, 'Sál Morava': 280, 'Sál A (KC)': 300, 'Sál B (KC)': 170,
        'A1, Stan bojovníků': 210,  'A1, Módní koutek': 30, 'A1, Digital art': 20, 'A1, stream': 608, 'Mimo sály': 50, 
        'A2, workshopy': 10
    }
    
    for loc_name, capacity in capacities.items():
        df_locs.loc[df_locs['name'] == loc_name, 'capacity'] = capacity    
    
    # fixing non-aligned names
    for name_from, name_to in get_names_to_replace().items():
        df_schedule.loc[df_schedule['name'] == name_from, 'name'] = name_to

    df_timetable = df_timetable.drop(columns=['animefestYearId', 'language'])
    df_locs = df_locs.drop(columns=['animefestYearId', 'language']).rename(columns={'name': 'location_name'})
    df_timetable = df_timetable.join(df_schedule, on='scheduleEntryId').join(df_locs, on='locationId')
    
    # there is consistency check for both info and fun suffixes, using any of them arbitratily
    df_timetable = df_timetable[(df_timetable['name'] + info_suffix).isin(df_form_columns)]  
    
    # todo: domigrovat sem čištění dat
    return df_timetable

def count_ratings(df_app, column, value):
    return df_app.groupby('název').apply(lambda x: (x[column] == value).sum())

def prepare_app_ratings(df_app):
    app_fun_ratings = pd.concat((count_ratings(df_app, 'fun', 1), count_ratings(df_app, 'fun', 2), count_ratings(df_app, 'fun', 3)), axis=1)
    app_fun_ratings.index += fun_suffix
    app_fun_ratings = app_fun_ratings.rename(columns={0: 'špatné', 1: 'v pohodě', 2: 'dobré'})
    app_fun_ratings = app_fun_ratings.T

    app_info_ratings = pd.concat((count_ratings(df_app, 'informace', 1), count_ratings(df_app, 'informace', 2), count_ratings(df_app, 'informace', 3)), axis=1)
    app_info_ratings.index += info_suffix
    app_info_ratings = app_info_ratings.rename(columns={0: 'špatné', 1: 'v pohodě', 2: 'dobré'})
    app_info_ratings = app_info_ratings.T
    
    app_ratings = pd.concat((app_fun_ratings, app_info_ratings), axis=1)
    app_ratings = app_ratings.reindex(sorted(app_ratings.columns), axis=1)
    
    app_ratings.loc['Nedostal(a) jsem se'] = 0
    
    return app_ratings

def merge_ratings(form_ratings, app_ratings):
    both_columns = list(set(form_ratings.columns).intersection(set(app_ratings.columns)))
    both_columns = pd.Series(both_columns)
    program_ratings = (form_ratings[both_columns] + app_ratings[both_columns]).fillna(0).astype(np.int32)
    program_ratings = program_ratings.reindex(sorted(program_ratings.columns), axis=1)
    
    attended_col = program_ratings.loc[['dobré', 'v pohodě', 'špatné']].fillna(0).sum(axis=0).rename('Zúčastnil(a) jsem se')
    
    program_attends = pd.concat((attended_col, program_ratings.loc['Nedostal(a) jsem se']), axis=1)
    
    program_columns = pd.Series(both_columns.str.replace(info_suffix, '', regex=False).str.replace(fun_suffix, '', regex=False).unique())

    return program_ratings, program_attends, program_columns

def calc_scores(program_ratings, program_columns):
    program_ratings_fun = program_ratings[program_columns + fun_suffix].loc[['dobré', 'špatné', 'v pohodě']].T.fillna(0)
    program_ratings_info = program_ratings[program_columns + info_suffix].loc[['dobré', 'špatné', 'v pohodě']].T.fillna(0)
    # optimization of dobré * 1 + v pohodě * 0 + špatné * -1
    program_fun_score = (program_ratings_fun['dobré'] - program_ratings_fun['špatné']) / program_ratings_fun.sum(axis=1)
    program_fun_score.index = program_fun_score.index.str.replace(fun_suffix, '', regex=False)
    
    program_info_score = (program_ratings_info['dobré'] - program_ratings_info['špatné']) / program_ratings_info.sum(axis=1)
    program_info_score.index = program_info_score.index.str.replace(info_suffix, '', regex=False)
    
    program_fun_score = program_fun_score.to_frame('score')
    program_fun_score['type'] = program_fun_score.index.to_series().map(col_to_category)

    program_info_score = program_info_score.to_frame('score')
    program_info_score['type'] = program_info_score.index.to_series().map(col_to_category)
    
    return program_fun_score, program_info_score