<h1 align="center">🚒Accident Detector🚒</h1>
<p align="center">  
 
<img src="https://gpvc.arturio.dev/Vanna-Ivision-2-0">

<img src="https://img.shields.io/badge/made%20by-Vanna-violet.svg" >

<img src="https://img.shields.io/badge/python-3.9 -red.svg">

<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >

<img src="https://img.shields.io/github/contributors/Vanna-Ivision-2-0/Vanna_Ivision_2_0.svg" >

<img src="https://img.shields.io/github/stars/Vanna-Ivision-2-0/Vanna_Ivision_2_0.svg?style=flat">

<img src="https://img.shields.io/github/languages/top/Vanna-Ivision-2-0/Vanna_Ivision_2_0.svg">

<img src="https://img.shields.io/github/issues/Vanna-Ivision-2-0/Vanna_Ivision_2_0.svg">

<img src="https://img.shields.io/github/watchers/Vanna-Ivision-2-0/Vanna_Ivision_2_0.svg?style=social&label=Watch">
 
</p>

<p align="center"><img  src="./readme_assets/logo_proj1.png" width="30%"></p>

## ***Навигация***
- [Описание](#описание)
- [Как пользоваться программой](#как_пользоваться)
- [Как это работает?](#как_это_работает)
- [О проекте и технологиях](#о_проекте_и_технологиях)
  - [Архитектура](#архитектура)
  - [Computer Vision & Machine Learning](#computer_vision_and_machine_learning)
  - [Результаты обучения модели](#обучение_модели)
- [Installation](#installation)
- [Возможные проблемы](#проблемы)

<a name="описание"></a> 
## ***Описание***

Программа реализована для распознавания ДТП на видеозаписях с камер наружного наблюдения. Дтп распознается как и с наличием специальной техники для фиксирования и помощи в ДТП, так и без каких-то четких опознавательных рамок. Возможна поддержка в "real-time" (онлайн режим).

С такой программой пользователь сможет заранее проверить ситуацию на дорогах, причину возникновения "пробки" и построить для себя удобный вариант маршрута.

Результаты работы видео с ДТП №1 с спецтранспортом  |  Результаты работы видео с ДТП №2 с спецтранспортом
:-------------------------:|:-------------------------:
![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/dtp.gif)  |  ![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/dtp2.gif)

Результаты работы видео с ДТП №3 без спецтранспорта |
:-------------------------:|
![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/NLwIPWmdGz.gif)  |

<a name="как_пользоваться"></a> 
## ***Как пользоваться программой***

1) Помещаем видео в папку videos.
<p align="left">
<img src="./readme_assets/1.jpg" width="40%"></p>

2) Преобразовываем видео в последовательность изображений (доступен Progress Bar).
<p align="left">
<img src="./readme_assets/2.jpg" width="60%"></p>

3) Запуск детектора объектов для всех директорий из videos2images. 
<p align="left">
<img src="./readme_assets/3.jpg" width="60%"></p>

4) Результаты работы детектора объектов.
<p align="left">
<img src="./readme_assets/4.jpg" width="60%"></p>

<p align="left">
<img src="./readme_assets/5.jpg" width="60%"></p>

5) Видеоподтверждения ДТП.
<p align="left">
<img src="./readme_assets/proof.jpg" width="40%"></p>

<a name="как_это_работает"></a> 
## ***Как это работает?***

Изначально, все видеофайлы из папки videos преобразуются в последовательность кадров. 
Первоначальный расчёт на то, что fps у тестовых видео будет такой же, как и у тех, что были предоставлены для исследование, т.е. 30. 
- Из видео каждую секунду берётся 2 кадра. 
- Затем последовательности кадров обрабатывается детектором объектов с порогом уверенности 0.7. Таким образом, в папке detection_results для всех видеофайлов, которые преобразовались в последовательность кадров, появятся результаты работы детектора объектов. В папке labels в каждом файле хранится информация о местонахождении объекта (bouning box) + уверенность (confidence).  
- Логика определения ДТП заключена в dtp.py. Мы считаем, что ДТП случилось в том случае, если на минимум 10 изображения был найден спецтранспорт с увереностью нейронной сети >=0.7. В случае наступления ДТП, в папке proof появится видеофайл, а также в консоль будет выведено соответствующее сообщение.

<a name="о_проекте_и_технологиях"></a> 
## ***О проекте и технологиях***

<a name="архитектура"></a> 
### Архитектура

<p align="left">
<img src="./readme_assets/photo_2022-01-29_19-15-05.jpg" width="30%"></p> 

<a name="computer_vision_and_machine_learning"></a> 
### Computer Vision & Machine Learning

**Технонологии**:
- [OpenCV](https://opencv.org/)
- [ffmpeg](https://www.ffmpeg.org/)
- [PyTorch](https://pytorch.org/)
- [YOLOv5](https://github.com/ultralytics/yolov5)
- [WandDB](https://wandb.ai/site)
- [Roboflow](https://roboflow.com/)

<a name="обучение_модели"></a> 
### Результаты обучения модели

*Метрики оценивания:*
<p align="left">
<img src="./readme_assets/метрики оценивания.jpg" width="60%"></p> 

![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/precconf.jpg)  |  ![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/recallconf.jpg)
:-------------------------:|:-------------------------:
![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/F1conf.jpg)  |  ![](https://github.com/Vanna-Ivision-2-0/Vanna_Ivision_2_0/blob/main/readme_assets/precrec.jpg)

*Результаты работы на валидационной выборке:*
<p align="left">
<img src="./readme_assets/detection.jpg" width="60%"></p>

*Train metrics:*
<p align="left">
<img src="./readme_assets/trainmetrix.jpg" width="60%"></p>

Confusion Matrix:
<p align="left">
<img src="./readme_assets/confusionmatrix.jpg" width="60%"></p>


<a name="installation"></a> 
## ***Installation***

- Установить пакеты из requirements.txt:

  `pip install –r requirements.txt`
- Скачать файлы моделей по [ссылке](https://drive.google.com/drive/folders/1SnG5JwYExb_aabh7PZWeJ14M50yia6uv?usp=sharing)
- Перенести их в weights

Протестировано для torch 1.9.0+cu111

<a name="проблемы"></a> 
## ***Возможные проблемы***

В случае, если алгоритм не определил ДТП, возможны следующие улучшения:
- Увеличения количество изображений при преобразовании из видео в изображения. 
python videos2imgs.py  --when 5
Таким образом, будет сохранен каждый 5-ый кадр, мы увеличим количество изображений в папках втрое. Повторить шаги, начиная с detect.
- Если ролики короткие и не применяли шаг выше, то следует изменить параметр --thresh для is_dtp.py на 7 или 5.
python is_dtp.py --thresh 7
- Если это не помогло, то изменяем confidence threshold для детектора объектов на 0.6
python detect.py  --conf-thres 0.6
Теперь python is_dtp.py --thresh 7 --conf 0.6
- В случае, если происходят ложные срабатывания, то увеличиваем параметры --thresh до 15-20 или
 --conf до 0.75-0.85.

Повторить все шаги выше, используя вторую модель из weights (yolo_hard_best.pt) для detect.py.
python detect.py --weights “weights/ yolo_hard_best.pt”

##
[![создано](https://github.com/Vanna-IVision/IVISION_HACK/blob/main/readme_asserts/created%20by-%20Anna-orange.svg)](https://github.com/elladiell) | [![создано](https://github.com/Vanna-IVision/IVISION_HACK/blob/main/readme_asserts/created%20by-Victor-blue.svg)](https://github.com/victor30608)


<p align="right" ><img src="./readme_assets/logo.png" width="40%"></p>

