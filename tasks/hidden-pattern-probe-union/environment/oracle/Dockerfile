FROM python:3.12-slim
RUN pip install --no-cache-dir networkx==3.4.2
COPY server.py instance.json /oracle/
RUN mkdir -p /state
ENV INSTANCE=/oracle/instance.json STATE_DIR=/state
EXPOSE 8080
HEALTHCHECK --interval=2s --timeout=3s --retries=30 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8080/status', data=b'{}'), timeout=2)"
CMD ["python", "/oracle/server.py"]
