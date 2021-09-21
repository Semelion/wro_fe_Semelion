#  Команда wro fe Semelion

## Описание техники
Мы команда из Москвы, изначально хотели создать робота на базе RC модели, но столкнулись с проблемами в подвеске.
Сейчас шасси робота собрана на лего, обратка зрения происходит с помощью камеры с углом обзора 170˚ на Raspberry pi4.
Также изначально мы использовали инфракрасные датчики растояния sharp, но на данный момент из-за шумов в показаниях решили отложить
их внедрение, для этого мы установили arduino uno, так как Raspberry не имеет АЦП. Изначально моторами управляли через Arduino, а даные
на неё отправляли по serial порту, но на данный момент управление серво приводом реализованно через GPIO Raspberry, а мотором сейчас идёт управление через Arduino.<br>
## Фотографии робота
![Фоточка с машиной общий план](/photos/ts7.jpg "?")<br>
![Погнали](/photos/ts1.jpg "?")<br>
![Фоточка с роботом](/photos/ts2.jpg "?")<br>
![Ещё фоточка с машинкой](/photos/ts3.jpg "?")<br>
![И опять](/photos/ts4.jpg "?")<br>
![Ну прям нафоткали](/photos/ts5.jpg "?")<br>
![Всё со всех сторон](/photos/ts6.jpg "?")<br>

## Наша команда
Нас в команде 2 человека:<br>
Конструктор и сисадмин: Трафняк Семён (@Semelion)<br>
![Фоточка с челиком1](/photos/TSL.jpg "?")<br>
Программист: Данила Морозов<br>
![Фоточка с челиком2](/photos/MD.jpg "?")<br>

## Программа
Код для обработки видео потока написан на языке питон с использованием библиотеки [Open CV](https://github.com/opencv/opencv).
Также для управления сервоприводом задействована библиотека [RPI.GPIO](https://pypi.org/project/RPi.GPIO/).
А для общения с Arduino использованна библиотека [pyserial](https://pypi.org/project/pyserial/).
Также нельзя пройти мимо проблемы автозапуска, мы столкнулись с проблеммой, что большая часть информации из статей не работала. 
Сейчас наш автозапуск устроен так: у нас есть .sh скрипт, который запускает код на питоне ([как написать код в этой статье](https://qna.habr.com/q/800529)), 
сам скрипт запускается вместе с оболочкой LXDE, сам файл автозапуска находится по адресу <code>/etc/xdg/lxsession/LXDE-pi/autostart</code>.
Потробнее про автозапуск есть в [этой статье](https://kakdelayut.ru/cifrovye-texnologii/kak-vypolnit-skript-pri-zapuske-na-raspberry-pi/).



# Team wro fe Semelion
## Description of the technique 
We are a team from Moscow, initially we wanted to create a robot based on an RC model, but we encountered problems in the suspension.
Now the chassis of the robot is assembled on Lego, the return of view is carried out using a camera with a 170˚ viewing angle on the Raspberry pi4.
Also, initially we used sharp infrared distance sensors, but at the moment, due to noise in the readings, we decided to postpone
their implementation, for this we installed arduino uno, since Raspberry does not have an ADC. Initially, the motors were controlled via the Arduino, and the data
it was sent to it via the serial port, but at the moment the control of the servo drive is implemented through the GPIO Raspberry, and the motor is now being controlled via the Arduino. <br> 
## Robot photos
![Фоточка с машиной](/photos/ts1.jpg "?")<br>
![Фоточка с роботом](/photos/ts2.jpg "?")<br>
![Ещё фоточка с машинкой](/photos/ts3.jpg "?")<br>
![И опять](/photos/ts4.jpg "?")<br>
![Ну прям нафоткали](/photos/ts5.jpg "?")<br>

## Our team
There are 2 people in the team: <br>
Constructor and sysadmin: Trafnyak Semyon (@Semelion) <br>
![Фоточка с челиком1](/photos/TSL.jpg "?")<br>
Programmer: Danila Morozov <br>
![Фоточка с челиком2](/photos/MD.jpg "?")<br>

## Program
The video stream processing code is written in Python using the [Open CV](https://github.com/opencv/opencv) library. The [RPI.GPIO](https://pypi.org/project/RPi.GPIO/) library is also used to control the servo drive. And to communicate with the Arduino, the [pyserial](https://pypi.org/project/pyserial/) library was used. Also, you cannot ignore the autorun problem, we ran into a problem that most of the information from the articles did not work. Now our autorun is arranged like this: we have a .sh script that runs the code in python ([how to write the code in this article](https://qna.habr.com/q/800529)), the script itself runs together with the LXDE shell, the autorun file itself is located at <code>/etc/xdg/lxsession/LXDE-pi/autostart</code>. More details about autorun are in this [article](https://kakdelayut.ru/cifrovye-texnologii/kak-vypolnit-skript-pri-zapuske-na-raspberry-pi/). 
