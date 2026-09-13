# CYBERLEEK Auxiliary Transaction Gateway Daemon
FROM python:3.11-slim

LABEL maintainer="CYBERLEEK Operations Syndicate"
LABEL challenge="Round 5 - The Attention Economy / The Money Trail"

WORKDIR /app

# Copy server daemon and ledger database
COPY ../service/cyberleek_service.py /app/cyberleek_service.py
COPY ../service/cyberleek_ledger.db /app/cyberleek_ledger.db

# Create unprivileged service user
RUN useradd -m -u 1001 cyberleek_daemon && \
    chown -R cyberleek_daemon:cyberleek_daemon /app

USER cyberleek_daemon

EXPOSE 9042

ENTRYPOINT ["python3", "-u", "/app/cyberleek_service.py"]
