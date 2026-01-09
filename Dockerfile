FROM python:3.13-alpine
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY app.py opdsfeedgen.py opds.toml ./
COPY content ./content

# Setup a bot user so the container doesn't run as the root user
RUN addgroup -S botgroup && adduser -S bot -G botgroup

# Change ownership to the bot user for all files
RUN chown -R bot:botgroup /usr/local/app

USER bot

CMD ["python", "-u", "app.py"]