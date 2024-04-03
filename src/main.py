import psycopg2

from src.config import config
from src.dbmanager import DBManager
from utils import (create_database, get_hh_data, get_hh_employers,
                   create_employers_table, create_vacancies_table,
                   insert_employers_data, insert_vacancies_data)


def main():
    db_name = 'hh_db'

    params = config()
    employers = get_hh_employers()
    vacancies = get_hh_data(employers)
    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_employers_table(cur)
                print("Таблица employers успешно создана")
                create_vacancies_table(cur)
                print("Таблица vacancies успешно создана")
                insert_employers_data(cur, employers)
                print("Данные в employers успешно добавлены")
                insert_vacancies_data(cur, vacancies)
                print("Данные в vacancies успешно добавлены")
        dbmanager = DBManager(params)
        print('\nCписок компаний:')
        dbmanager.get_companies_and_vacancies_count()
        print('\nСписок вакансий:')
        dbmanager.get_all_vacancies()
        print('\nСредняя зарплата по вакансиям от/до:')
        dbmanager.get_avg_salary()
        print('\nCписок вакансий, у которых зарплата выше средней:')
        dbmanager.get_vacancies_with_higher_salary()
        word = input('\nВведите слово для поиска вакансий: ').title()
        print('Cписок вакансий, соответствующих требованию:')
        dbmanager.get_vacancies_with_keyword(word)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()
