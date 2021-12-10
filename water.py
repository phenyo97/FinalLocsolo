# External module imp
import RPi.GPIO as GPIO
import datetime
import time
import sys
 
init = False

GPIO.setmode(GPIO.BOARD) # GPIO pin board módban

#Utolsó öntözés lekérdezése
def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "Nem volt még öntözve!"

#Szenzor lekérdezése
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

#Pin beállítása
def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    
def auto_water(tank, delay = 6, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    #Felhasználó edényének kapacitás bekérése 
    waterPerPulse = 25 # 1 löket 25ml vízet nyom
    
    pulse = tank * 1000 / waterPerPulse * 0.75 #Max löketszám  víz elfogyása ellen (tartály 75%-a)
    
    overWaterPrev = tank * 1000 / waterPerPulse * 0.50 #Max löketszám  túlöntözés ellen (tartály 50%-a)
    
    consecutiveMax = 0 #Felhasznált löketek száma
    
    init_output(pump_pin)
    print("Fut! Kilépéshez nyomja meg a CTRL+Z-t")
    try:
        while  consecutive_water_count < overWaterPrev and consecutiveMax < pulse:
            time.sleep(delay)
            wet = get_status(pin = water_sensor_pin) == 0
            if not wet:
                pump_on(pump_pin, 1)
                consecutive_water_count += 1
                consecutiveMax += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt: # CTRL+Z lenyomására kilépés
        print("\nKilépés")
        GPIO.cleanup() # cleanup all GPI

#Egy löket víz a pumpából/ fájlba írás
def pump_on(pump_pin = 7, delay = 1):
    init_output(pump_pin)
    f = open("last_watered.txt", "w")
    f.write("Utolsó öntözés: {}".format(datetime.datetime.now()))
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pump_pin, GPIO.HIGH)
