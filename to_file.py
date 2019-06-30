import csv
import time

count = 0
while True:
    data = {'title': '{}'.format(count), 'content': count}
    with open('test.csv', 'a+') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'content'])
        writer.writerow(data)
    count += 1
    time.sleep(1)