class VisualizeQuestions(object):
    def __init__(self):
        from preprocessor.database import Database

        database = Database(
            'host',
            'db',
            'user',
            'pass',
            'utf8mb4'
        )

        self.connection = database.connect_with_pymysql()

    def view_source_by_month_data(self, year):
        import pandas as pd
        import numpy as np
        numpy_list = []
        if self.connection:
            with self.connection.cursor() as cursor:
                for month in range(1, 13):
                    sql = "SELECT source,count(id) as count FROM questions WHERE YEAR(created_at) = "+str(year)+" AND MONTH(created_at) = "+str(month)+" group by source"
                    cursor.execute(sql)
                    result = cursor.fetchall()

                    if result:
                        new_list = []
                        for i in result:
                            new_list.append(i['count'])
                        numpy_list.append(new_list)
        return pd.DataFrame(np.array(numpy_list), columns=['web', 'app', 'internet.org', 'm-site'])

    def view_source_by_month(self, year):
        import matplotlib.pyplot as plt
        plt.style.use('ggplot')
        df2 = self.view_source_by_month_data(year)
        df2.plot.bar()
        plt.show()

    def connection_close(self):
        self.connection.close()


if __name__ == '    __main__':
    a = VisualizeQuestions()
    a.view_source_by_month(2016)
    a.connection_close()
