short int light1 = 10;
short int light2 = 11;
short int light3 = 12;
int s = 0;


void setup() {
    pinMode(light1, OUTPUT);
    pinMode(light2, OUTPUT);
    pinMode(light3, OUTPUT);
    digitalWrite(light1, LOW);
    digitalWrite(light2, LOW);
    digitalWrite(light3, LOW);
    delay(250);
    digitalWrite(light1, HIGH);
    delay(250);
    digitalWrite(light2, HIGH);
    delay(250);
    digitalWrite(light3, HIGH);
    delay(250);
    digitalWrite(light1, LOW);
    digitalWrite(light2, LOW);
    digitalWrite(light3, LOW);
    SerialUSB.begin(2);


}

void loop() {
    if (SerialUSB.available() > 0){
        s = SerialUSB.read();
        if (s == 97) {
            digitalWrite(light1, HIGH);
        }
        if (s == 98) {
            digitalWrite(light1, LOW);
        }
        if (s == 99) {
            digitalWrite(light2, HIGH);
        }
        if (s == 100) {
            digitalWrite(light2, LOW);
        }
        if (s == 101) {
            digitalWrite(light3, HIGH);
        }
        if (s == 102) {
            digitalWrite(light3, LOW);
        }
        SerialUSB.println(s);
    }
}