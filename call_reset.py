from reset import factory_reset
import threading
import time

#Devices = ['9089f948']
Devices = ['39e25973', '96104d9d', 'b341002c','9089f948']
threads = []
for device in Devices:
	t = threading.Thread(target =factory_reset , args = (device,))
	threads.append(t)
#excute thread
for i in range(len(Devices)):
	threads[i].start()
#wait for end of t
for i in range(len(Devices)):
	threads[i].join()

print("complete")
time.sleep(30)