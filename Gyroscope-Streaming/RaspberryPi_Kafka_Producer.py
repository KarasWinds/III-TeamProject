#!/usr/bin/python3

import smbus2 as smbus
import time
import sys
import threading
from kafka import KafkaProducer


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def read_data():
    datatime = time.time()
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    total = str(datatime) + "," + str(gyro_xout)+","+str(gyro_yout)+","+str(gyro_zout)+","\
            +str(accel_xout)+","+str(accel_yout)+","+str(accel_zout)
    return total


def datasend():
    print("Start sending messages")
    while True:
        if input_kb == 'stop':  # stop
            # 結束連線
            producer.flush()
            producer.close()
            bus.close()
            break
        try:
            rawdata = read_data()
            producer.send(topic=topic_name, key=None, value=rawdata)
        except Exception:
            e_type, e_value, e_traceback = sys.exc_info()
            print("type ==> %s" % e_type)
            print("value ==> %s" % e_value)
            print("traceback ==> file name: %s" % e_traceback.tb_frame.f_code.co_filename)
            print("traceback ==> line no: %s" % e_traceback.tb_lineno)
            print("traceback ==> function name: %s" % e_traceback.tb_frame.f_code.co_name)
            continue
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    # Power management registers
    power_mgmt_1 = 0x6b

    bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
    address = 0x68       # This is the address value read via the i2cdetect command

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    # Kafka Producer setting
    producer = KafkaProducer(
        # Kafka集群在那裡?
        bootstrap_servers=["IP:9092"],
        # 指定msgKey的序列化器, 若Key為None, 無法序列化, 透過producer直接給值
        # key_serializer=str.encode,
        # 指定msgValue的序列化器
        value_serializer=str.encode)
    topic_name = "user1"
    input_kb = ''
    ds = threading.Thread(target=datasend)
    ds.start()
    while True:
        print("Please enter 'stop' to stoping process")
        input_kb = str(sys.stdin.readline()).strip("\n")
        if input_kb == 'stop':  # stop
            break
    ds.join()
    print("End process")