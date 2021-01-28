
FROM mcr.microsoft.com/mssql/server:latest


LABEL mantainer="Fabio Galvagni"
LABEL release-date="28-01-2021"


ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=1234qwerASDF

COPY ./db /

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]

CMD [ "/opt/mssql/bin/sqlservr" ]

EXPOSE 1433/tcp