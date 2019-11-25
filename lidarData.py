from lidar_lite import Lidar_Lite
from firebase import firebase
lidar = Lidar_Lite()

connected = lidar.connect(1)
tempRaw = lidar.getVelocity()
tempAbs = abs(tempRaw)
dist = lidar.getDistance()
if tempAbs > 99:
        tempAbs %= 10

firebase= firebase.FirebaseApplication('https://lidarspeedometer.firebaseio.com/')
firebase.post('/data', { "Distance":str(dist), "velocity":str(tempAbs)})
print dist
