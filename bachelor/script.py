import argparse
from readline import insert_text
import subprocess


def mulBias(bias, start, end):
	with open(path,'r') as f:
		t1 = f.readlines()

	t1[172] = '    _imu._gyro[instance] = gyro * ' + str(bias) + ';}\n'
	t1[454] = '    _imu._accel[instance] = accel * ' + str(bias) + ';}\n'
	t1.insert(172, '\n')
	tmp = '    if ((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + ')) {'
	t1.insert(172, tmp)
	t1.insert(456, '\n')
	t1.insert(456, tmp)

	tmp = '    _imu._gyro[instance] = gyro;'
	tmp2 = '    _imu._accel[instance] = accel;'
	t1.insert(172, '\n')
	t1.insert(172, tmp)
	t1.insert(458, '\n')
	t1.insert(458, tmp2)

	
	with open(path, 'w') as f:
		f.writelines(t1)


def addBias(bias, start, end):
	with open(path,'r') as f:
		t1 = f.readlines()

	t1[172] = '    _imu._gyro[instance] = gyro + ' + str(bias) + ';}\n'
	t1[454] = '    _imu._accel[instance] = accel + ' + str(bias) + ';}\n'
	t1.insert(172, '\n')
	tmp = '    if ((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + ')) {'
	t1.insert(172, tmp)
	t1.insert(456, '\n')
	t1.insert(456, tmp)

	tmp = '    _imu._gyro[instance] = gyro;'
	tmp2 = '    _imu._accel[instance] = accel;'
	t1.insert(172, '\n')
	t1.insert(172, tmp)
	t1.insert(458, '\n')
	t1.insert(458, tmp2)

	with open(path, 'w') as f:
		f.writelines(t1)

def stall(start, end):
	with open(path,'r') as f:
		t1 = f.readlines()
	
	t1.insert(172, '\n')
	tmp = '    if (!((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + '))) {'
	t1.insert(172, tmp)
	t1.insert(175, '	}\n')
	t1.insert(457, '\n')
	tmp = '    if (!((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + '))) {'
	t1.insert(457, tmp)
	t1.insert(460, '	}\n')

	with open(path, 'w') as f:
		f.writelines(t1)


def replay(capture, start, end):
	with open(path,'r') as f:
		t1 = f.readlines()
	t1.insert(11, 'Vector3f _capturedGyro;\n')
	t1.insert(12, 'Vector3f _capturedAccel;\n')

	tmp =  '    if (((AP_HAL::millis() >= ' + str(capture) + ') && (AP_HAL::millis() <= ' + str(capture + 500) + '))) {\n    _capturedGyro = gyro;}\n'
	tmp += '	if (((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + '))) {\n    _imu._gyro[instance] = _capturedGyro;}\n'
	t1.insert(175, tmp)
	
	tmp = '    if (((AP_HAL::millis() >= ' + str(capture) + ') && (AP_HAL::millis() <= ' + str(capture + 500) + '))) {\n    _capturedAccel = accel;}\n'
	tmp += '	if (((AP_HAL::millis() >= ' + str(start) + ') && (AP_HAL::millis() <= ' + str(end) + '))) {\n    _imu._accel[instance] = _capturedAccel;}\n'
	t1.insert(458, tmp)
	with open(path, 'w') as f:
		f.writelines(t1)






def deleteStuff():
	with open('./original/AP_InertialSensor_Backend.cpp','r') as f:
		t1 = f.readlines()
	
	with open(path, 'w') as f:
		for line in t1:
			f.write(line)


#line 173 (-1): gyro data is written
#line 455 (-1): accel data is written




parser = argparse.ArgumentParser(description="attack script on SITL library.\n Example use: ./script.py -stall 120000 124000 \n Note: in case of error, run this script with sudo", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-delete", action="store_true", help="clean up attack code from the library")
parser.add_argument("-mulBias", type=float, help="insert multiplication bias")
parser.add_argument("-addBias", type=float, help="insert addition bias")
parser.add_argument("-stall", action="store_true", help="stall attack")
parser.add_argument("start", type=int, help='attack time frame start in milliseconds')
parser.add_argument("end", type=int, help='attack time frame end in milliseconds')
parser.add_argument("-replay", type=int, help='replay attack, insert time in milliseconds where data is captured for later replay')

path = '../libraries/AP_InertialSensor/AP_InertialSensor_Backend.cpp'
args = parser.parse_args()
config = vars(args)
deleteStuff()
if config['mulBias']:
	mulBias(config['mulBias'], config['start'], config['end'])
elif config['addBias']:
	addBias(config['addBias'], config['start'], config['end'])
elif config['stall']:
	stall(config['start'], config['end'])
elif config['replay']:
	replay(config['replay'], config['start'], config['end'])




with open('log.txt', 'w') as fout:
	with open('errors.txt', 'w') as errout:
		subprocess.call("./run-tests.sh -l ./scriptlogs", shell=True, stdout=fout, stderr=errout)




if config['delete']:
	deleteStuff()

