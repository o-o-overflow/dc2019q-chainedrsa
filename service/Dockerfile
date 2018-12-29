from ubuntu:18.04
run echo "travis_fold:start:Dapt\033[33;1mservice Dockerfile apt\033[0m" && \
    apt-get update && apt-get install -y python xinetd libssl-dev \
    netcat vim && \
    echo "\ntravis_fold:end:Dapt\r"

copy src/service /service
copy src/keys_bak /keys
# copy src/preprocess.py /preprocess.py
copy src/work.py /work.py
copy service.conf /service.conf
copy banner_fail /
copy src/wrapper /wrapper

run touch /flag && chmod 644 /flag && echo "OOO{pr0f35510n4l_r54_br34k3r}" > /flag
run mkdir flags
# run touch /tmp/keys && chmod 666 /tmp/keys
# run ln -s /tmp/keys /keys 
run chmod 644 /keys
# run python preprocess.py /flag /keys_bak
# run chmod 644 flags/*
# run chmod -R 644 keys_bak/*
# run rm -rf flag preprocess.py

expose 5000
cmd ["/usr/sbin/xinetd", "-filelog", "log", "-dontfork", "-f", "/service.conf"]
