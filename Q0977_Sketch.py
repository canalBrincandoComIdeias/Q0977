#     AUTOR:    BrincandoComIdeias
#     APRENDA:  https://cursodearduino.net/
#     SKETCH:   Servo Motor
#     DATA:     06/01/23

from machine import Pin
from machine import ADC
from machine import PWM
from utime import sleep_ms as delay

# Configurando joystick
pinCTRLX = machine.ADC(27)
pinCTRLY = machine.ADC(26)
pinCTRLZ = machine.Pin(22, Pin.IN, Pin.PULL_UP)

# Equivalente a função map()
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# ================ Classe Servo ================
class Servo:
    
    # Construtor
    def __init__(self):
        self.FREQ = 50
        self.pulse_min = 2000 # 0º ~ 0.61 ms
        self.pulse_max = 7800 # 180º ~ 2.38 ms
        self.duty = self.pulse_min + (self.pulse_max - self.pulse_min) #90º
    
    # Configura o pino e inicia o PWM a 90º
    def attach(self, pino):
        self.pin = Pin(pino)
        self.pwm = PWM(self.pin)
        self.pwm.freq(self.FREQ)
        self.pwm.duty_u16(self.duty)
    
    # Converte o angulo em pulso
    def convert(self, angulo):
        if angulo <= 0:
            return self.pulse_min
        if angulo >= 180:
            return self.pulse_max
        
        pulso = self.pulse_min + int( (angulo / 180) * (self.pulse_max - self.pulse_min) )
        return pulso
    
    # Recebe o angulo e controla o servo
    def write(self, angulo):
        self.duty = self.convert(angulo)
        self.pwm.duty_u16(self.duty)
        
# ================ Classe Servo ================

# Configurando Servo
garra = Servo()
pulso = Servo()
braco = Servo()
base  = Servo()

garra.attach(2) # Angulo inicial 90º
pulso.attach(3) # Angulo inicial 90º
braco.attach(6) # Angulo inicial 90º
base.attach(7)  # Angulo inicial 90º

posX = 90
posY = 90
estadoGarra = 1
posZAnt = 1

neutroX = 86
neutroY = 86
faixaNeutra = 10

while True:
    leituraX = pinCTRLX.read_u16() # 0 ~ 65535
    anguloX = map(leituraX, 0, 65535, 180, 0)
    
    if anguloX > (neutroX + faixaNeutra):
        posX = posX + ((((anguloX - faixaNeutra) - neutroX) / 10)) ** 1
        posX = int(min(posX, 180))
    
    if anguloX < (neutroX - faixaNeutra):
        posX = posX - (((neutroX - (anguloX + faixaNeutra)) / 10)) ** 1
        posX = int(max(posX, 0))
        
    leituraY = pinCTRLY.read_u16() # 0 ~ 65535
    anguloY = map(leituraY, 0, 65535, 0, 180)
    
    if anguloY > (neutroY + faixaNeutra):
        posY = posY + ((((anguloY - faixaNeutra) - neutroY) / 10)) ** 1
        posY = int(min(posY, 180))
        
    if anguloY < (neutroY - faixaNeutra):
        posY = posY - (((neutroY - (anguloY - faixaNeutra)) / 10)) ** 1
        posY = int(max(posY, 0))
        
    base.write(posX)
    braco.write(max(posY, 50))
    pulso.write(posY)
    
    posZ = pinCTRLZ.value()
    if posZ and not posZAnt:
        estadoGarra = not estadoGarra
    
    if estadoGarra:
        garra.write(80)
    else:
        garra.write(40) #45
    
    posZAnt = posZ
    
    #print(f"LeituraX: {leituraX}\t AnguloX: {anguloX}\t PosX: {posX}\t LeituraY: {leituraY}\t AnguloY: {anguloY}\t PosY: {posY}   ", end='\r')
    delay(50) # delay de 50mS