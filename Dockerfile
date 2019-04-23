# Author: Cláudio Ferreira Carneiro
# LNLS - Brazilian Synchrotron Light Source Laboratory
FROM lnlscon/pydm:v1.6.5

LABEL maintainer="Claudio Carneiro <claudio.carneiro@lnls.br>"

RUN mkdir -p /opt/pydm-opi
WORKDIR /opt/pydm-opi

ENV PATH /opt/epics-R3.15.5/base/bin/linux-x86_64:$PATH
ENV EPICS_BASE /opt/epics-R3.15.5/base
ENV EPICS_HOST_ARCH linux-x86_64
ENV EPICS_CA_AUTO_ADDR_LIST YES

COPY requirements.txt .

RUN echo 'y\n' | pip3 uninstall pydm

RUN apt-get update &&      \
    apt-get install -y     \
    qt5-default            \
    pyqt5-dev-tools        \
    python3-pyqt5          \
    python3-pyqt5.qtsvg    \
    python3-pyqt5.qtwebkit \
    qttools5-dev-tools     \
    vim

RUN pip3 install PyQt5==5.7.1
RUN pip3 install -r requirements.txt
RUN cd /opt/pydm-1.6.5 && pip3 install .[all]

CMD /opt/pydm-opi/launch.sh
