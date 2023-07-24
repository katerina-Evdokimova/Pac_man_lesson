Pac-man
---
Проект реализован в рамках преподавания курса "Введение в GameDev" на площадке РТУ МИРЭА ДТ "Альтаир".

---

ТЗ:
-
    -   Главный экран:
        -   Выбор режима (прям на главном экране) - после клика начинается игра.
            -   Бесконечный. Поле не ограничено. Игрок проигрывает только в случае налета на приведение. Нет - выигрыша.
            -   Стандартный. Поле ограничено. Игрок проигрывает, если попадает в приведение. Выигрыш - после прохождения всех уровней.
        -   Рейтинг(реализовать в отдельном окне)
            -   Возможность просматривать рейтинг для разных режимов
            -   Возможность просматривать общий рейтинг из всех таблиц
        -   Настройки. (Возможность вкл. или выключить звук)
    -   Экран рейтинга:
        -   Данные подтягиваются из БД
        -   Четыре кнопки - стандартный режим, бесконечный, общаяб выход в меню
        -   Столбцы: 1. id; 2. date/time; 3. score - в бесконечном и общей
        -   В стандартном добавляется еще уровень.
    -   Экран игры:
        -   В правом верхнем углу очки
        -   При нажатии на “P” - en - игра ставится на паузу
        -   При нажатии на esc - выход в меню(с сохранением результата)
        -   Спамится уровень:
            1. Лабиринт, на каждой клетке точка в одной из клеток персонаж в нескольких других (в зависимости от уровня от 1 до 5) приведения.
            2. Перемещение персонажа происходит за счет стрелок
            3. Приведения двигаются произвольно
            4. При столкновении персонажа и приведения - выпадают частицы и пишется GAME OVER
            5. При столкновении персонажа и точки начисляются очки.
            6. Все точки собраны - следующий уровень( в случае обычной игры). В бесконечном режиме - поле постоянно расширяется.
            7. Персонаж в обычном режиме не может перейти за пределы экрана
        -   Персонаж и приведения - должны быть анимированы.
        -   Движение персонажа: один клик - одна клетка
        -   Перемещение приведения: плавно передвигается по клеткам,те примерно по 1/8(любое) клетки.
        -   После проигрыша или выигрыша - результаты записываются в БД
    -  БД. Реализовать как вам удобнее, но рекомендую сделать две таблицы.
        1. Бесконечный режим: id, data, score
        2. Стандартный режим: id, data, level, score


---
Основные директории
-

* _*data*_ - в данной директории хранятся необходимые изображения для игры
* _*data_db*_ - директория для основных файлов при работе с БД
* _*db*_ - директория для хранения файла с БД
* _*sounds*_ - директория для хранения звуков
* _*data_level*_ - необходима для хранения уровней