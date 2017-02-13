# nvml-cloudwatch
This utility collects GPU metrics from NVIDIA management library (NVML) and sends them to CloudWatch

```
docker run -d \
-e aws_access_key_id=$cloudwatch_aws_access_key_id \
-e aws_secret_access_key=$cloudwatch_aws_secret_access_key \
--device /dev/nvidia0:/dev/nvidia0 \
--device /dev/nvidia1:/dev/nvidia1 \
--device /dev/nvidia2:/dev/nvidia2 \
--device /dev/nvidia3:/dev/nvidia3 \
--device /dev/nvidia4:/dev/nvidia4 \
--device /dev/nvidia5:/dev/nvidia5 \
--device /dev/nvidia6:/dev/nvidia6 \
--device /dev/nvidia7:/dev/nvidia7 \
--device /dev/nvidiactl:/dev/nvidiactl \
--device /dev/nvidia-uvm:/dev/nvidia-uvm \
-v /usr/lib64/nvidia/libnvidia-ml.so:/usr/lib64/libnvidia-ml.so:ro \
-v /usr/lib64/nvidia/libnvidia-ml.so.1:/usr/lib64/libnvidia-ml.so.1:ro \
-v /usr/lib64/nvidia/libnvidia-ml.so.367.48:/usr/lib64/libnvidia-ml.so.367.48:ro \
--cpuset-cpus "0" \
--memory 512m \
--memory-swap 0m \
-h $(docker-machine active) \
--restart unless-stopped \
--name nvml-cloudwatch docker.synapse.org/syn5644795/nvml-cloudwatch 
```
