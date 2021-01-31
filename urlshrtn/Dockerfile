

FROM ubuntu:latest


LABEL mantainer="Fabio Galvagni"
LABEL release-date="28-01-2021"


# update the linux distribution
RUN apt update -y
RUN apt upgrade -y
RUN apt install wget -y
RUN apt install htop -y


# install conda
RUN cd ~
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN mkdir -p /opt/miniconda3
RUN bash ~/miniconda3/miniconda.sh -b -u -p /opt/miniconda3
RUN rm -rf ~/miniconda3/ # rm -rf ~/miniconda3/miniconda.sh
ENV PATH="/opt/miniconda3/bin:${PATH}"
RUN conda init bash

RUN conda update --all -y
	
# COPY ./urlshrtn/environment.yml /root/
# RUN /opt/miniconda3/bin/conda env create -f ~/environment.yml
RUN conda install flask -y
RUN conda install pymssql -y
RUN conda install sqlalchemy -y


# python scripts
RUN mkdir /opt/urlshrtn
COPY ./urlshrtn/*.py /opt/urlshrtn/


# automatically run the webserver
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "base", "python", "/opt/urlshrtn/main.py"]



# EXPOSE 8080/tcp