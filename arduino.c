//write the code in arduino that will take  2,3,4,5 pins as inputs in binary pin num 2 is 2^1 and output pwn onpin 9, do1% 15% 25% 50% 75% 100% pwm, you dont to use all the pins

int pin1 = 2;
int pin2 = 3;
int pin3 = 4;
int pin4 = 5;
int pwm = 9;
int val = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
  pinMode(pin3, INPUT);
  pinMode(pin4, INPUT);
  pinMode(pwm, OUTPUT);
  Serial.begin(9600);
}

void loop() {
    int input = (digitalRead(pin1) << 0) | (digitalRead(pin2) << 1) | (digitalRead(pin3) << 2) | (digitalRead(pin4) << 3);//15 10 5
    
    switch (input) {//do 15%,14%,13%,12%....1
        case 1:
            val = 255*0.01;
            break;
        case 2:
            val = 255*0.02;
            break;
        case 3:
            val = 255*0.03;

        default:
            val = 0;
            break;


    }
    
    analogWrite(pwm, val);
    delay(100); // Add a small delay to avoid rapid changes
    Serial.println(val);
    


    
}

