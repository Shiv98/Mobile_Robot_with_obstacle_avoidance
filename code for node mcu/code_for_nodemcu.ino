const int trigPin = D2;
const int echoPin = D1;

float duration;
float d;
int ir1=D6;
int ir2=D7;
int val1;
int val2;
int pwm1;
int pwm2;
void setup() 
{
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
pinMode(ir1,OUTPUT);
pinMode(ir2,OUTPUT);
Serial.begin(115200);

}

void loop() {

digitalWrite(trigPin, LOW);
delayMicroseconds(2);

digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

duration = pulseIn(echoPin, HIGH);

d= duration*0.84/2;


//val1=(-4.62256619/10000)*d*d+(2.15371388/10)*d+(3.56264173*10);
//val2=(-2.57794842/10000)*d*d+(1.32340015/10)*d+(9.50539516*10);

val1=(4.62256619/10000)*d*d+(2.15371388/10)*d+(3.56264173*10);
val2=(-2.57794842/10000)*d*d+(1.32340015/10)*d+(9.50539516*10);

pwm1=abs(val1/61*1024);
pwm2=abs(val2/112*1024);

analogWrite(ir1,pwm1);
delay(100);
analogWrite(ir2,pwm2);
delay(100);
Serial.println(pwm1);
Serial.println(pwm2);
Serial.println(d);
}
