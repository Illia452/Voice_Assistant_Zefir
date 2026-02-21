import arrow
import time


# Твій epoch (наприклад, отриманий з бази або сервера)
timestamp = 1771510000
print(timestamp)

# Перетворюємо в об'єкт Arrow
t = arrow.get(timestamp)

# 1. Дізнаємося відносно "зараз" (українською!)
print(t.humanize(locale='uk')) 
# Виведе щось типу: "2 години тому", "вчора", "8 днів тому"

# 2. Перевірка логікою
if t.date() == arrow.now().shift(days=-1).date():
    print("Це було вчора")
