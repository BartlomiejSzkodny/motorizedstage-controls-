//write code to controll by pwm analog 0 arduino
int pwmPin = 9; // PWM pin connected to analog 0

void setup() {
    pinMode(pwmPin, OUTPUT);
}

void loop() {
    analogWrite(pwmPin, 128); // Set PWM to 50% duty cycle
}
