from datetime import datetime

from flask_migrate import Migrate, init, migrate, upgrade
# init -
# migrate - generate an initial migration
# upgrade - apply the migration to the database
# $ flask db init/migrate/upgrade
# Each time the database models change repeat the migrate and upgrade commands
# https://github.com/miguelgrinberg/flask-migrate

from src.utils.config import Config
from src.models import db, User, Test, Question
from src.models.tables.questions import AnswerTypeEnum
from src import create_flask_app

if __name__ == '__main__':
    config = Config('config.yaml', '.env')
    app = create_flask_app(config.flask)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(User('admin', '2345', 'Alex', 'admin@example.com'))
        db.session.add(User('fuest', '2345', 'Alex', 'guest@example.com'))

        db.session.add(Test(
            'История России',
            'Тест по основным датам и события из истории Русского государства, Российской империи, СССР и современной Российской Федерации.',
            datetime.fromisoformat('2022-10-25 23:00'),
            datetime.fromisoformat('2122-10-25 23:00')
        ))
        db.session.add(Test(
            'Всемирная история',
            'В данном тесте предлагается проверить знания по всемирной истории от Античности до современной истории. Среди вопросов будут варианты со свободным ответом и с единственным и множественным выбором ответов.',
            datetime.fromisoformat('2022-11-27 23:00'),
            datetime.fromisoformat('2122-10-27 23:00')
        ))
        db.session.add(Test(
            'title',
            'description',
            datetime.fromisoformat('2022-12-29 23:00'),
            datetime.fromisoformat('2023-10-29 23:00')
        ))
        db.session.commit()

        db.session.add(Question(1, 'Выберите все цвета флага России', AnswerTypeEnum.many_select, ['красный','белый','синий','жёлтый'], ['белый','синий','красный']))
        db.session.add(Question(1, 'Кто был последним российским императором?', AnswerTypeEnum.one_select, ['Александр 2','Николай 1','Николай 2'], ['Николай 2']))
        db.session.add(Question(1, 'В каком году умер Сталин?', AnswerTypeEnum.one_select, ['1939','1943','1949', '1953'], ['1953']))
        db.session.add(Question(1, 'В каком году был основан город Санкт-Петербург?', AnswerTypeEnum.free_field, [], ['1703']))
        db.session.add(Question(1, 'Выберите все прежние названия города Санкт-Петербург', AnswerTypeEnum.many_select, ['Петроград', 'Ленинград', 'Кировоград', 'Новый Петербург'], ['Петроград', 'Ленинград']))

        db.session.add(Question(2, 'Год основания города Рим', AnswerTypeEnum.one_select, ['817 год до н. э.', '753 год до н. э.', '719 год до н. э.'], ['753 год до н. э.']))
        db.session.add(Question(2, 'Традиционной датой падения Западной Римской империи считается', AnswerTypeEnum.one_select, ['362','401','476','513'], ['476']))
        db.session.add(Question(2, 'Условным окончанием античности и началом средних веков (средневековья) считается', AnswerTypeEnum.one_select, ['Падение Западной Римской империи', 'византия', 'признание христианства'], ['Падение Западной Римской империи']))
        db.session.add(Question(2, 'В каком году произошёл захват Константинополя и падение Византии (Восточная Римская империя)?', AnswerTypeEnum.free_field, [], ['1453']))
        db.session.add(Question(2, 'В каком году была открыта Америка Христофором Колумбом?', AnswerTypeEnum.one_select, ['1485', '1492', '1498', '1501'], ['1492']))
        db.session.add(Question(2, 'В каком году произошла Октябрьская революция?', AnswerTypeEnum.one_select, ['1913', '1915', '1917', '1919'], ['1917']))
        db.session.add(Question(2, 'В каком году закончилась первая мировая война?', AnswerTypeEnum.free_field, [], ['1918']))
        db.session.add(Question(2, 'Отметьте учатстников Антанты в первой мировой войне', AnswerTypeEnum.many_select, ['Российская империя', 'Великобритания', 'Франция', 'Германия', 'США'], ['Российская империя', 'Великобритания', 'Франция']))
        db.session.add(Question(2, 'В каком году закончилась вторая мировая война?', AnswerTypeEnum.one_select, ['1939','1941','1944', '1945'], ['1945']))
        db.session.add(Question(2, 'В каком году прекратил существование СССР и образовалось СНГ?', AnswerTypeEnum.free_field, [], ['1991']))

        db.session.commit()
