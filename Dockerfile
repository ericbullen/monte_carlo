FROM fedora:34
LABEL maintainer="eric.bullen@gmail.com"

RUN dnf update -y && dnf install -y \
        glibc-common \
        glibc-langpack-en \
        python3-tabulate \
        python3-numpy \
    && dnf clean all

ENV TZ="America/Los_Angeles"
ENV LANG="en_US.utf8"

COPY FinanceFuture.py monte_carlo.py /srv/

USER nobody

ENV LOWER_PCT=".96"
ENV MAX_YEARS="100"
ENV RUNS="10000"

CMD ["python3", "/srv/monte_carlo.py"]
