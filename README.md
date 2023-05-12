  <h3 align="center">Packaged Food Explorer</h3>

  <p align="center">
    GUI Application that explore and analyze packaged food dataset
    <br>
    <a href="[https://world.openfoodfacts.org/data](https://world.openfoodfacts.org/data)">Data Source</a>
    
</p>


## Table of contents

- [Table of contents](#table-of-contents)
- [Feature](#feature)
- [Quick start](#quick-start)
- [What's included](#whats-included)
- [How to use](#how-to-use)
- [Used library and modules](#used-library-and-modules)
- [GUI](#gui)
- [UML Class Diagram and Design Pattern](#uml-class-diagram-and-design-pattern)
- [Example of sequence diagram](#example-of-sequence-diagram)
- [NOTE](#note)

## Feature

- Filter and plot data of each product

## Quick start
- Clone github repository
```
git clone https://github.com/Sosokker/Food-Nutrient-Viewer-Tkinter
```
- pip install
```py
# pip
pip install -r requirements.txt
```
- To start GUI window run app.py
```py
python app.py
```

## What's included

```text
Main/
│── Essential/
│   ├── descriptive.py
│   ├── FoodSearch.py
│   ├── networkgraphprob.ipynb
│   ├── plotter.py
│   ├── prepare_db.py
│   ├── data/
│   │   ├── food_data.db
│   │   │── japan_data.csv
│   │   │── thai_data.csv
│   │   │── us_data_1.csv
│   │   │── us_data_2.csv
│   │   │── us_data_3.csv
│   │   └── us_data_4.csv
│── resources/
│   ├──loading.gif
│   ├──notfound.png
│   └──gui_main.png 
│── app.py
│── main.ipynb
│── requirements.txt
└── README.md
```
## How to use

## Used library and modules

- tkinter
- sqlite3
- plotly
- matplotlib
- pandas
- numpy
- pillow

## GUI

![GUI](/resources/gui_main.png)

## UML Class Diagram and Design Pattern

![UML](/resources/UML-Class-Diagram-Facade.png)

- Use Facade Design Pattern

## Example of sequence diagram

![Seq](/resources/sequnce-diagram-plotter.png)

## NOTE

- Process data with file [main.ipynb](/main.ipynb) need .csv file from [Data Source](https://world.openfoodfacts.org/data)

- If error about "food_data.db" occur download [food_data.db](https://drive.google.com/file/d/1QuVPKZVv0UGEHdH2AYX9g7D-vh3YZCAM/view?usp=share_link) and put in folder [data](/Essential/data/)
