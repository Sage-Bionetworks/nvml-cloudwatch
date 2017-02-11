#!/usr/local/bin/python2.7
# encoding: utf-8
from pynvml import *
import time
import os
import boto3

if __name__ == "__main__":
    sys.exit(main())
    
    
def signal_handler(signal, frame):
    print('Shutting down.')
    sys.exit(1)

def main(argv=None):
    nvmlInit()
    #c = statsd.StatsClient(os.environ['statsd_host'], 8125)
    cwc = boto3.client('cloudwatch')

    
    print "Driver Version:", nvmlSystemGetDriverVersion()
    deviceCount = nvmlDeviceGetCount()

    while (True):
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            info = nvmlDeviceGetMemoryInfo(handle)
            cwc.put_metric_data(namespace="nnvida",name="gpu.memory.total-"+str(i),unit='Bytes',info.total)
            cwc.put_metric_data(namespace="nnvida",name="gpu.memory.free-"+str(i),unit='Bytes',info.free)
            cwc.put_metric_data(namespace="nnvida",name="gpu.memory.used-"+str(i),unit='Bytes',info.used)
            # performance state is an enum. See https://docs.nvidia.com/deploy/pdf/NVML_API_Reference_Guide.pdf
            cwc.put_metric_data(namespace="nnvida",name="gpu.power.state-"+str(i),unit='None',nvmlDeviceGetPerformanceState(handle))
            # power usage is in milliwatts.  See https://docs.nvidia.com/deploy/pdf/NVML_API_Reference_Guide.pdf
            cwc.put_metric_data(namespace="nnvida",name="gpu.power.usage-"+str(i),unit='None',nvmlDeviceGetPowerUsage(handle))
            cwc.put_metric_data(namespace="nnvida",name="gpu.temperature-"+str(i),unit='None',nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU))
            # clock info is an enum.   See https://docs.nvidia.com/deploy/pdf/NVML_API_Reference_Guide.pdf
            cwc.put_metric_data(namespace="nnvida",name="gpu.clock.graphics-"+str(i),unit='None',nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS))
            # clock sm is actually MHz.  See https://docs.nvidia.com/deploy/pdf/NVML_API_Reference_Guide.pdf
            cwc.put_metric_data(namespace="nnvida",name="gpu.clock.sm-"+str(i),unit='None',nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM))
            cwc.put_metric_data(namespace="nnvida",name="gpu.clock.mem-"+str(i),unit='Bytes',nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM))
            info = nvmlDeviceGetUtilizationRates(handle)
            cwc.put_metric_data(namespace="nnvida",name="gpu.utilization.gpu-"+str(i),unit='Bytes',info.gpu)
            cwc.put_metric_data(namespace="nnvida",name="gpu.utilization.memory-"+str(i),unit='Bytes',info.memory)
    
        print "NVML metrics pushed to CloudWatch"
        time.sleep(60)

    nvmlShutdown()
    return 0

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    sys.exit(main())
