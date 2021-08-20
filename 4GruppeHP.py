import RPi.GPIO as GPIO
import datetime
import time
import board
import busio
import adafruit_ina260
import pigpio
import sys

def run(mv1,mv2,mv3,mv4):


    #test connection with screen
    # f = open("demofile2.txt", "a")
    # f.write(mv1)
    # f.write(mv2)
    # f.write(mv3)
    # f.write(mv4)
    # f.close()

    #_____________________________________________________________________________________________
    # Setup

    # Initialize voltage sensors
    ina260_1 = adafruit_ina260.INA260(0x40)
    ina260_2 = adafruit_ina260.INA260(0x41)
    ina260_3 = adafruit_ina260.INA260(0x44)
    ina260_4 = adafruit_ina260.INA260(0x43)

    # Initialize dokument for logbook
    date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    file = open("Watchdog.txt", "w")
    file.write(str("Out of range from " + date))
    file.flush()

    # Tell the library which pin nunbering system you are going to use
    GPIO.setmode(GPIO.BCM)

    # Initialize pins
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)

    # Initialize variables 
    duty1 = 0
    duty2 = 0
    duty3 = 0
    duty4 = 0

    i = 0
    log_state = 1
    prev_log_state = 1

    # Initialize Gruppe 1
    tagtet_voltage1 = (mv1)
    Gruppe1 = GPIO.PWM(12, 1000)
    Gruppe1.start(duty1)

    # Initialize Gruppe 2
    tagtet_voltage2 = (mv2)
    Gruppe2 = GPIO.PWM(13, 1000)
    Gruppe2.start(duty2)

    # Initialize Gruppe 3
    tagtet_voltage3 = (mv3)
    Gruppe3 = GPIO.PWM(19, 1000)
    Gruppe3.start(duty3)

    # Initialize Gruppe 4
    tagtet_voltage4 = (mv4)
    Gruppe4 = GPIO.PWM(16, 1000)
    Gruppe4.start(duty4)


    #_____________________________________________________________________________________________
    # Tanks Are runnng
    while 1:
        
        # Group 1
        # If voltage measurement is higer/lower than taget add/subtract from duty 
        if int(ina260_1.voltage*1000) < int(tagtet_voltage1) :
            duty1 = duty1 + 0.01
        elif int(ina260_1.voltage*1000) > int(tagtet_voltage1) :
            duty1 = duty1 - 0.01
            
        # Duty max is 100 and min is 0
        if duty1 <= 0 :
            duty1 = 0  
        elif duty1 >= 100 :
            duty1 = 100
        
        # Change duty
        Gruppe1.ChangeDutyCycle(duty1)
        
        # Group 2
        if int(ina260_2.voltage*1000) < int(tagtet_voltage2) :
            duty2 = duty2 + 0.01
        elif int(ina260_2.voltage*1000) > int(tagtet_voltage2) :
            duty2 = duty2 - 0.01
            
        # Duty max is 100 and min is 0
        if duty2 <= 0 :
            duty2 = 0  
        elif duty2 >= 100 :
            duty2 = 100
        
        # Change duty
        Gruppe2.ChangeDutyCycle(duty2)
        
        # Group 3
        if int(ina260_3.voltage*1000) < int(tagtet_voltage3) :
            duty3 = duty3 + 0.01
        elif int(ina260_3.voltage*1000) > int(tagtet_voltage3) :
            duty3 = duty3 - 0.01
            
        # Duty max is 100 and min is 0
        if duty3 <= 0 :
            duty3 = 0  
        elif duty3 >= 100 :
            duty3 = 100
        
        # Change duty
        Gruppe3.ChangeDutyCycle(duty3)
        
        # Group 4
        if int(ina260_4.voltage*1000) < int(tagtet_voltage4) :
            duty4 = duty4 + 0.01
        elif int(ina260_4.voltage*1000) > int(tagtet_voltage4) :
            duty4 = duty4 - 0.01
            
        # Duty max is 100 and min is 0
        if duty4 <= 0 :
            duty4 = 0  
        elif duty4 >= 100 :
            duty4 = 100
        
        # Change duty
        Gruppe4.ChangeDutyCycle(duty4)

        #______________________________________________________________________________________________
        # Watchdog (Only for gruppe 1)

    
        if ina260_1.voltage*1000 > int(tagtet_voltage1)-100 and ina260_1.voltage*1000 < int(tagtet_voltage1)+100 :
            log_state = 0
        elif ina260_1.voltage*1000 < int(tagtet_voltage1)-100 or ina260_1.voltage*1000 > int(tagtet_voltage1)+100 :
            log_state = 1
            

        if log_state != prev_log_state :
            date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
            if log_state == 0 :
                file.write(str(" to " + date) + '\n')
                file.flush()
            elif log_state == 1 :
                file.write(str("Out of range from " + date))
                file.flush()

        prev_log_state = log_state
        #_____________________________________________________________________________________________
        
        # After 1000 loops print voltage of tank 1
        i = i + 1
        if i == 10000:
            i = 0  
            print(int(ina260_1.voltage*1000))


if __name__ == '__main__':
    print("helloo")
    run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])