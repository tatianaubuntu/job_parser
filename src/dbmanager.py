import psycopg2


class DBManager:
    """Класс для работы с данными в БД"""
    def __init__(self, params):
        """Конструктор подключения к базе данных"""
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий
        у каждой компании"""
        self.cur.execute('''
                            SELECT a.name, COUNT(b.*) as number_of_vacancies
                            FROM employers a
                            LEFT JOIN vacancies b
                            ON a.id = b.employer_id
                            GROUP BY a.name
                            ORDER BY COUNT(b.*) DESC
                            ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'{row[0]} (вакансий - {row[1]})')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute('''
                            SELECT a.name, a.salary_from, a.salary_to, a.url,
                                   b.name as employer_name
                            FROM vacancies a
                            LEFT JOIN employers b
                            ON a.employer_id = b.id
                            ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'{row[0]}, зарплата от {row[1]} до {row[2]}, '
                  f'ссылка: {row[3]}, работодатель: {row[4]}')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute('''
                        SELECT ROUND(AVG(salary_from)) AS average_salary_from,
                        ROUND(AVG(salary_to)) AS average_salary_to
                        FROM vacancies
                        ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'{row[0]}/{row[1]}')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям"""
        self.cur.execute('''
                            SELECT *
                            FROM vacancies
                            WHERE salary_from >
                            (SELECT AVG(salary_from) FROM vacancies)
                            ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def get_vacancies_with_keyword(self, word):
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова"""
        self.cur.execute(f'''
                            SELECT *
                            FROM vacancies
                            WHERE name LIKE '{word}%'
                            ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
