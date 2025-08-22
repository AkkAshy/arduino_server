// Геркон (D2) + PIR (D4) + датчик разбития стекла (D7) + SIM800L (HTTP POST)

const int PIN_REED   = 2;   // геркон
const int PIN_PIR    = 4;   // датчик движения
const int PIN_GLASS  = 7;   // датчик разбития стекла

// --- Геркон (антидребезг) ---
const unsigned long DEBOUNCE_MS = 30;
int stableReed = HIGH;     
int lastReed = HIGH;
unsigned long lastChangeReed = 0;

// --- PIR ---
unsigned long lastPirTrigger = 0;
const unsigned long PIR_COOLDOWN = 5000; // 5 секунд пауза

// --- Стекло ---
int lastGlass = HIGH; // HIGH = норма, LOW = тревога

// --- HTTP ---
unsigned long lastHttpTime = 0;
const unsigned long HTTP_COOLDOWN = 15000; // 15 сек между запросами

// 🔹 сюда впиши свой сервер
const char APN[]     = "internet";           // APN твоего оператора
const char SERVER[]  = "123.45.67.89";       // IP или домен Django
const char URL[]     = "/api/event/";        // эндпоинт

void setup() {
  pinMode(PIN_REED, INPUT_PULLUP);
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_GLASS, INPUT_PULLUP);

  Serial.begin(9600);    
  Serial1.begin(9600);   // SIM800L

  while (!Serial) {}

  Serial.println("Система: геркон + PIR + стекло + SIM800L (HTTP)");

  initSIM800L();
}

void loop() {
  // --- Геркон ---
  int reading = digitalRead(PIN_REED);
  if (reading != lastReed) {
    lastChangeReed = millis();
    lastReed = reading;
  }
  if ((millis() - lastChangeReed) >= DEBOUNCE_MS && reading != stableReed) {
    stableReed = reading;
    printReed(stableReed);
    if (stableReed == HIGH) sendEvent("door", "open");
  }

  // --- PIR ---
  int pirState = digitalRead(PIN_PIR);
  if (pirState == HIGH && (millis() - lastPirTrigger) > PIR_COOLDOWN) {
    Serial.println("PIR: Движение обнаружено!");
    sendEvent("motion", "detected");
    lastPirTrigger = millis();
  }

  // --- Стекло ---
  int glassState = digitalRead(PIN_GLASS);
  if (glassState != lastGlass) {
    lastGlass = glassState;
    printGlass(glassState);
    if (glassState == LOW) sendEvent("glass", "broken");
  }

  delay(50);
}

// ------------------ Функции ------------------

void initSIM800L() {
  delay(1000);
  sendAT("AT");
  sendAT("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
  sendAT("AT+SAPBR=3,1,\"APN\",\"" + String(APN) + "\"");
  sendAT("AT+SAPBR=1,1");   // открыть GPRS
  delay(2000);
  sendAT("AT+SAPBR=2,1");   // проверить соединение
  Serial.println("SIM800L инициализирован для GPRS");
}

void sendEvent(const char* sensor, const char* state) {
  if (millis() - lastHttpTime < HTTP_COOLDOWN) return; // антиспам
  lastHttpTime = millis();

  String json = String("{\"sensor\":\"") + sensor + "\",\"state\":\"" + state + "\"}";

  Serial.print("POST -> ");
  Serial.println(json);

  sendAT("AT+HTTPINIT");
  sendAT("AT+HTTPPARA=\"CID\",1");
  sendAT("AT+HTTPPARA=\"URL\",\"http://" + String(SERVER) + String(URL) + "\"");
  sendAT("AT+HTTPPARA=\"CONTENT\",\"application/json\"");

  Serial1.println("AT+HTTPDATA=" + String(json.length()) + ",10000");
  delay(200);
  Serial1.println(json);
  delay(1000);

  sendAT("AT+HTTPACTION=1");  // 1 = POST
  delay(5000);
  sendAT("AT+HTTPTERM");
}

void sendAT(String cmd) {
  Serial1.println(cmd);
  delay(500);
  while (Serial1.available()) {
    Serial.write(Serial1.read()); // вывод ответа модуля
  }
}

void printReed(int state) {
  if (state == LOW) {
    Serial.println("ГЕРКОН: Дверь ЗАКРЫТА");
  } else {
    Serial.println("ГЕРКОН: Дверь ОТКРЫТА");
  }
}

void printGlass(int state) {
  if (state == HIGH) {
    Serial.println("СТЕКЛО: Норма");
  } else {
    Serial.println("СТЕКЛО: РАЗБИТО!");
  }
}
