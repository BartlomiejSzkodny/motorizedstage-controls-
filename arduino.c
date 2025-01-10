//write code to controll by pwm analog 0 arduino
int pwmPin = 9; // PWM pin connected to analog 0

void setup() {
    pinMode(pwmPin, OUTPUT);
    pinMode(13, INPUT);
}

void loop() {
    if (digitalRead(13) == HIGH) {
        analogWrite(pwmPin, 255); // Set PWM to 100% duty cycle
    } else {
    analogWrite(pwmPin, 0); // Set PWM to 50% duty cycle
    }
}
