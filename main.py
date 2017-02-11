#!/usr/local/bin/python2.7
# encoding: utf-8
from pynvml import *
import os
import boto3
import signal
import time

def signal_handler(signal, frame):
    print('Shutting down.')
    sys.exit(1)

def main(argv=None):
    nvmlInit()
    #c = statsd.StatsClient(os.environ['statsd_host'], 8125)
    cwc = boto3.client('cloudwatch', aws_access_key_id=os.environ['aws_access_key_id'], aws_secret_access_key=os.environ['aws_secret_access_key'], region_name='us-east-1')

    
    print "Driver Version:", nvmlSystemGetDriverVersion()
    deviceCount = nvmlDeviceGetCount()
    host=os.getenv('HOSTNAME')

    while (True):
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            info = nvmlDeviceGetMemoryInfo(handle)
            utilizationInfo = nvmlDeviceGetUtilizationRates(handle)
            cwc.put_metric_data(Namespace='nvidia',MetricData=[
                {'MetricName':'gpu.memory.total','Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':info.total,'Unit':'Bytes'},
                {'MetricName':"gpu.memory.free", 'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':info.free, 'Unit':'Bytes'},
                {'MetricName':"gpu.memory.used",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':info.used,'Unit':'Bytes'},
                {'MetricName':"gpu.power.state",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetPerformanceState(handle)},
                {'MetricName':"gpu.power.usage",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetPowerUsage(handle)},
                {'MetricName':"gpu.temperature",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)},
                {'MetricName':"gpu.clock.graphics",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)},
                {'MetricName':"gpu.clock.sm",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)},
                {'MetricName':'gpu.clock.mem','Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM),'Unit':'Bytes'},
                {'MetricName':"gpu.utilization.gpu",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':utilizationInfo.gpu,'Unit':'Bytes'},
                {'MetricName':"gpu.utilization.memory",'Dimensions':[{'Name':'host','Value':host},{'Name':'device','Value':str(i)}],'Value':utilizationInfo.memory,'Unit':'Bytes'}
            ])
    
        print "NVML metrics pushed to CloudWatch"
        time.sleep(60)

    nvmlShutdown()
    return 0

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    sys.exit(main())
