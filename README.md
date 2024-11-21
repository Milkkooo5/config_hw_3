# Конфигурационное управление

### Домашнее задание 3
#### Условие задания
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на учебном конфигурационном языке принимается из
стандартного ввода. Выходной текст на языке json попадает в стандартный
вывод.

Однострочные комментарии:

|| Это однострочный комментарий

Многострочные комментарии:
<!--
Это многострочный
комментарий
-->
Словари:

{

 имя = значение;

 имя = значение;
 
 .имя = значениеъ
 ...
 
}

Имена:

[_a-zA-Z]+

Значения:

• Числа.

• Словари.

Объявление константы на этапе трансляции:
var имя := значение;

Вычисление константы на этапе трансляции:

6

@(имя)


Результатом вычисления константного выражения является значение.
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2
примера описания конфигураций из разных предметных областей.



#### Основные функции

Суть данного кода заключается в создании парсера для конфигурационных файлов, который обрабатывает текстовый ввод, извлекает переменные и формирует JSON-объект.

Вот ключевые аспекты работы этого парсера:

1. Удаление комментариев: Код начинает с очистки входного текста от комментариев, чтобы оставить только действительные данные.

2. Обработка констант: Он ищет объявления констант в формате var имя := значение;, извлекает их и сохраняет в словаре. Это позволяет использовать эти константы в дальнейшем.

3. Замена ссылок на константы: В тексте ищутся ссылки на константы в формате @(<имя_константы>), и они заменяются на соответствующие значения, что делает текст более гибким.

4. Парсинг конфигурации: Основная часть парсинга заключается в извлечении ключей и значений из текстового представления словаря, позволяя обрабатывать как простые значения (числа, строки), так и вложенные структуры (другие словари).

5. Формирование JSON: После обработки конфигурации результат преобразуется в формат JSON, что делает его удобным для хранения и передачи данных.


#### Примеры работы 

Пример конфигурации веб-сервера

![image](https://github.com/user-attachments/assets/e49a2d82-6693-4f2a-a86f-0b5664c98c57)


![image](https://github.com/user-attachments/assets/ec429a5b-dc10-440a-ad28-dd86ac350a78)


Пример конфигурации облачного хранилища


![image](https://github.com/user-attachments/assets/a74de07d-f756-419e-86d9-41378333c963)


![image](https://github.com/user-attachments/assets/9989534d-5007-4047-b931-44d5fbb0e750)

Пример с многострочным комментарием

![{307C7D22-942E-4876-9BA7-A03D03867132}](https://github.com/user-attachments/assets/f183d545-99b8-485e-931f-e8581332e924)



![{5F333738-4F1E-4443-9972-C4767EBC9861}](https://github.com/user-attachments/assets/1283ffcc-1d6f-419f-9136-2d28bb35ae1e)



#### Результаты тестирования 

Для выполнения тестов воспользуемся библиотекой unittest 

![image](https://github.com/user-attachments/assets/40c13ba9-1572-4015-af03-f0ed0e686d4e)


Также фрагменты кода с тестами

![image](https://github.com/user-attachments/assets/e80048c3-6524-4701-81cb-1506f9e6de6b)

![image](https://github.com/user-attachments/assets/c1e5e2cf-59b5-416d-8e0d-7b15e44a9470)










