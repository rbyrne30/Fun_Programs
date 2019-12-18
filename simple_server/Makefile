C = gcc
CFLAGS = -pthread
CLIENT_O = echoclient
SERVER_O = echoserver
CLIENT_C = echoclient.c
SERVER_C = echoserver.c

all: $(CLIENT_O) $(SERVER_O)

$(CLIENT_O): $(CLIENT_C)
	$(C) $(CFLAGS) -o $(CLIENT_O) $(CLIENT_C)

$(SERVER_O): $(SERVER_C)
	$(C) $(CFLAGS) -o $(SERVER_O) $(SERVER_C)

clean:
	rm -f $(CLIENT_O) $(SERVER_O)
