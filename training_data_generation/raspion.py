import datetime
import time
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
from flask import Flask,render_template,request

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
app = Flask(__name__)

TRIG=29
ECHO=31
IRL=33
IRR=35

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(IRL,GPIO.IN)
GPIO.setup(IRR,GPIO.IN)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/readValue")
def sendValues():
	file=open("DataLog.txt",'a')
	IRL_Value=str(GPIO.input(IRL))
	IRR_Value=str(GPIO.input(IRR))
	US=str(ultrasonic())
	Speed=speed(datetime.datetime.now())
	LS=Speed[Speed.index("L=")+2:Speed.index(" ")]
	RS=Speed[Speed.index(" ")+3:]
	value="RPM of Left Motor:"+LS+" RPM of Right Motor:"+RS+" Ultrasonic Distance:"+US
	file.write(str(datetime.datetime.now())+" "+value+"\n")
	ServerValues=RS+"#"+LS+"%"+US
	print(ServerValues)
	return ServerValues

def speed(T):
	stateL=GPIO.input(IRL)
	stateR=GPIO.input(IRR)
	countL=0
	countR=0

	while (datetime.datetime.now()-T).total_seconds()*1000<500:
		if GPIO.input(IRL)==1-stateL:
			countL+=1
			stateL=1-stateL
		if GPIO.input(IRR)==1-stateR:
			countR+=1
			stateR=1-stateR

	speedL=countL*15
	speedR=countR*15
	return "L="+str(speedL)+" R="+str(speedR)

def ultrasonic():
	GPIO.output(TRIG,False)
	time.sleep(0.0002)
	GPIO.output(TRIG,True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)
	while GPIO.input(ECHO)==0:
		pulse_start=time.time()
	while GPIO.input(ECHO)==1:
		pulse_end=time.time()
	pulse_duration=pulse_end-pulse_start
	distance=pulse_duration*17150
	distance=int(round(distance,2))
	if distance>400:

		distance=400
	return distance

if __name__=="__main__":
	app.run(host='0.0.0.0',port=8000,debug=True)