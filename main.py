from machine import Pin
from machine import I2C
import ssd1306
from time import sleep
import neopixel
from machine import PWM
import time
import math

tempo = None
atomos = None
pin = None
i = None
meia_vida = None
lista_tempo = None
lista_atomos = None
idx = None

pIn5=Pin(5, Pin.IN, Pin.PULL_UP)

pIn10=Pin(10, Pin.IN, Pin.PULL_UP)


tempo = 0
atomos = 24
meia_vida = 30
pin = 7
lista_tempo = []
lista_atomos = []
lista_tempo.append(0)
lista_atomos.append(24)

i2c=I2C(1, scl=Pin(3), sda=Pin(2))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)
oled.text('Decaimento', 20, 0)
oled.show()
oled.text('Tempo', 0, 20)
oled.show()
oled.text((str(tempo) + ''), 60, 20)
oled.show()
oled.text('Atomos', 0, 40)
oled.show()
oled.text((str(atomos) + ''), 60, 40)
oled.show()

np=neopixel.NeoPixel(Pin(pin),25)
for i in range(24):
  np[i]=(0,25,0)
np.write()
pwm21 = PWM(Pin(21))
pwm21.freq(2000)
while True:
  if (pIn5.value()) == 0:
    atomos = atomos / 2
    tempo = tempo + meia_vida
    lista_tempo.append(tempo)
    lista_atomos.append(atomos)
    for i in range(24):
      np[i]=(0,0,0)
    i = 0
    for count in range(int(atomos)):
      np[i]=(0,25,0)
      i = i + 1
    np.write()
    oled.fill(0)
    oled.text('Decaimento', 20, 0)
    oled.show()
    oled.text('Tempo', 0, 20)
    oled.show()
    oled.text((str(tempo) + ''), 60, 20)
    oled.show()
    oled.text('atomos', 0, 40)
    oled.show()
    oled.text((str(atomos) + ''), 60, 40)
    oled.show()
    time.sleep_ms(300)
  if (pIn10.value()) == 0:
    oled.fill(0)
    idx = 0
    for count2 in range(int(len(lista_tempo))):
      oled.text('.', (int((round(lista_tempo[int(idx)] / 2)))), (int((round(60 - lista_atomos[int(idx)] * 2)))))
      oled.show()
      idx = idx + 1
    time.sleep_ms(300)
  if round(atomos) > 0:
    pwm21.duty_u16(32768)
    time.sleep_ms(15)
    pwm21.duty_u16(0)
    time.sleep_ms(int((120 / (atomos + 0.1))))
  time.sleep_ms(10)
