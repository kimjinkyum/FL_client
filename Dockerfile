#FROM arm64v8/ubuntu:18.04
FROM nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3
#RUN apt-get install python3-setuptools
#RUN easy_install3 pip

# ENV LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu/tegra

COPY main.py .
COPY init_fl.py .
COPY model.py .
COPY utils.py .
RUN pip3 install flask
ENTRYPOINT ["python3", "main.py"]
