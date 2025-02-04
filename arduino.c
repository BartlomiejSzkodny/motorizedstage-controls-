int inputPin = 9; // Input pin
int outputPin = 13; // Output pin

void setup() {
    pinMode(inputPin, INPUT);
    pinMode(outputPin, OUTPUT);
}

void loop() {
    if (digitalRead(inputPin) == HIGH) {
        digitalWrite(outputPin, HIGH); // Set pin 13 high
    } else {
        digitalWrite(outputPin, LOW); // Set pin 13 low
    }
}
