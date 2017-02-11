#!/usr/local/bin/python2.7
# encoding: utf-8
from pynvml import *
import time
import os
import boto3
import signal

def signal_handler(signal, frame):
    print('Shutting down.')
    sys.exit(1)

def main(argv=None):
    nvmlInit()
    #c = statsd.StatsClient(os.environ['statsd_host'], 8125)
    cwc = boto3.client('cloudwatch', region_name='us-east-1')

    
    print "Driver Version:", nvmlSystemGetDriverVersion()
    deviceCount = nvmlDeviceGetCount()
    host=os.getenv("host")

    while (True):
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            info = nvmlDeviceGetMemoryInfo(handle)
            utilizationInfo = nvmlDeviceGetUtilizationRates(handle)
            cwc.put_metric_data(Namespace=host,MetricData=[
                {'MetricName':'gpu.memory.total-'+str(i),'Dimensions':[{"host":host}],'Value':info.total,'Unit':'Bytes'},
                {'MetricName':"gpu.memory.free-"+str(i), 'Dimensions':[{"host":host}],'Value':info.free, 'Unit':'Bytes'},
                {'MetricName':"gpu.memory.used-"+str(i),'Dimensions':[{"host":host}],'Value':info.used,'Unit':'Bytes'},
                {'MetricName':"gpu.power.state-"+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetPerformanceState(handle)},
                {'MetricName':"gpu.power.usage-"+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetPowerUsage(handle)},
                {'MetricName':"gpu.temperature-"+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)},
                {'MetricName':"gpu.clock.graphics-"+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)},
                {'MetricName':"gpu.clock.sm-"+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)},
                {'MetricName':'gpu.clock.mem-'+str(i),'Dimensions':[{"host":host}],'Value':nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM),'Unit':'Bytes'},
                {'MetricName':"gpu.utilization.gpu-"+str(i),'Dimensions':[{"host":host}],'Value':utilizationInfo.gpu,'Unit':'Bytes'},
                {'MetricName':"gpu.utilization.memory-"+str(i),'Dimensions':[{"host":host}],'Value':utilizationInfo.memory,'Unit':'Bytes'}
            ])
    
        print "NVML metrics pushed to CloudWatch"
        time.sleep(60)

    nvmlShutdown()
    return 0

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    sys.exit(main())
