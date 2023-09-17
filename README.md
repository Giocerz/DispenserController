# Dispenser Controller
The project is about a digital controller for a sugar dispenser which uses a servo motor and a strain gauge, uses arduino and app in python, where connect through serial communication. This project was developed that final project of Discrete Control course at Universidad Popular del Cesar.
## Used Technology
- Python: PyQT5
- Arduino.

## Use
### Python run
- First clone this project and type the following in a terminal in the project directory:
```
virtualenv env
./env/Scripts/activate
pip install -r requirements.txt
```
### Arduino code
- Use the code that is in <a href='https://github.com/Giocerz/DispenserController/blob/main/Arduino/CONTROLADOR_DISPENSADOR/CONTROLADOR_DISPENSADOR.ino'>controlador.ino</a> in arduino IDE and upload your sketch in your Arduino board. Modify according to your requeriments.
- Remember install <a href='https://github.com/bogde/HX711'>HX711 library</a>

### Components in this project

|Arduino uno|1kg load cell|ADC HX711|180 degree servomotor s90|
|-----------|-------------------------------------|-------------------------|-------------------------|
|<img src='https://store.arduino.cc/cdn/shop/products/A000066_03.front_934x700.jpg?v=1629815860' width='150'/>|<img src='https://robu.in/wp-content/uploads/2017/04/517saYIG0vL._SL1100_.jpg' width='150'/>|<img src='https://electronilab.co/wp-content/uploads/2017/11/M%C3%B3dulo-conversor-Anal%C3%B3gico-Digital-de-24-Bits-HX711-1.jpg' width='150'/>|<img src='https://www.electronicoscaldas.com/1120/micro-servo-motor-sg90.jpg' width='150'/>|



- Also can use a nano.
- Use a servo according to your requeriments.
- It's recommended not to use the arduino for a servo source.


## Authors
- Giovanni Caicedo (Giocerz)
- Andres Gonzales
- Stefania Velez
- Manuel Varon
