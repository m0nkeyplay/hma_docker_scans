FROM ubuntu
WORKDIR /mnt
ENV TZ=US/Central
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt upgrade -y
RUN apt install -y tzdata wget curl
RUN apt update && apt upgrade -y
RUN apt install -y fping openvpn unzip
RUN apt update && apt upgrade -y
RUN apt install -y  python3 
RUN apt update && apt upgrade -y
RUN apt install -y python3-pip
RUN apt install -y nmap
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt update
RUN apt install -y google-chrome-stable
RUN BROWSER_MAJOR=$(google-chrome --version | sed 's/Google Chrome \([0-9]*\).*/\1/g') && \
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${BROWSER_MAJOR} -O chrome_version && \
    wget https://chromedriver.storage.googleapis.com/`cat chrome_version`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    DRIVER_MAJOR=$(chromedriver --version | sed 's/ChromeDriver \([0-9]*\).*/\1/g') && \
    echo "chrome version: $BROWSER_MAJOR" && \
    echo "chromedriver version: $DRIVER_MAJOR" && \
    if [ $BROWSER_MAJOR != $DRIVER_MAJOR ]; then echo "VERSION MISMATCH"; exit 1; fi
RUN apt update && apt upgrade -y
COPY requirements.txt /mnt
RUN  pip3 install --no-cache-dir -r requirements.txt
RUN apt autoremove
ENTRYPOINT [ "/bin/bash", "-l" ]