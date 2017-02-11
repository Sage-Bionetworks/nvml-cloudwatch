# nvml-cloudwatch
This utility collects GPU metrics from NVIDIA management library (NVML) and sends them to CloudWatch
```
Run using `nvidia-docker`: https://github.com/NVIDIA/nvidia-docker

nvidia-docker run -d \
-v /path/to/aws/creds:/root/.aws/credentials:ro \
--restart unless-stopped \
--cpuset-cpus "0" \
--memory 512m \
--memory-swap 0m \
--name nvml-cloudwatch docker.synapse.org/syn5644795/nvml-cloudwatch 

