FROM ollama/ollama

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    ollama serve & \
    pid=$!; \
    while ! curl -s http://127.0.0.1:11434 > /dev/null; do \
        echo "Waiting for Ollama server to be ready..."; \
        sleep 1; \
    done; \
    ollama pull llama3.2:3b; \
    kill $pid; \
    wait $pid