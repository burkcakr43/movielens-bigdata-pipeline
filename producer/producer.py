import json
import time
import csv
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

dosya_yolu = dosya_yolu = '../data/ml-25m/ml-25m/ratings.csv'
hiz = 50  # saniyede kaç mesaj gönderilsin

print("Producer başladı...")

with open(dosya_yolu, 'r') as f:
    reader = csv.DictReader(f)
    sayi = 0
    for satir in reader:
        mesaj = {
            "userId": int(satir['userId']),
            "movieId": int(satir['movieId']),
            "rating": float(satir['rating']),
            "timestamp": int(satir['timestamp']),
            "event_type": "rating_submitted"
        }
        producer.send('movielens-ratings', value=mesaj)
        sayi += 1

        if sayi % 1000 == 0:
            print(f"{sayi} mesaj gönderildi")

        time.sleep(1 / hiz)

producer.flush()
print("Bitti!")

