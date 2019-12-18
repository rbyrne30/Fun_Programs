// I pledge my honor that I have abided by the Stevens Honor System.
// Ryan Byrne

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
 
#define MAXPENDING 10
#define MAXMSG 256

int main(int argc, char *argv[]) {
  // Takes in one argument: <server_port number>
  if (argc != 2) {
    printf("Usage: %s <server_port>\n", argv[0]);
    return 1;
  }

  int server_port = atoi(argv[1]);

  // Create server socket
  int server_socket;
  if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
    perror("Socket creation");
    exit(EXIT_FAILURE);
  }

  // Define server address
  struct sockaddr_in server_address;
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(server_port);
  server_address.sin_addr.s_addr = INADDR_ANY;

  // Bind socket to specified server_port
  if (bind(server_socket, (struct sockaddr*) &server_address, sizeof(server_address)) < 0) {
    perror("Binding");
    exit(EXIT_FAILURE);
  }

  // Listen on socket
  if (listen(server_socket, MAXPENDING) < 0) {
    perror("Listening");
    exit(EXIT_FAILURE);
  }

  printf("Server listening on port %d\n", server_port);

  // Create client array
  fd_set read_fds, write_fds;
  FD_ZERO(&write_fds);
  FD_SET(server_socket, &write_fds);


  // Monitor sockets
  struct sockaddr_in clientname;
  int size;

  while (1) {
    read_fds = write_fds;

    // Check events
    if (select (MAXPENDING, &read_fds, NULL, NULL, NULL) < 0) {
      perror("select()");
      exit(EXIT_FAILURE);
    }

    // Check new requests
    for (int i = 0; i < FD_SETSIZE; i++) {
      if (FD_ISSET(i, &read_fds)) {
        // New connection request on original socket
        int new;
        size = sizeof(clientname);
        new = accept(server_socket, (struct sockaddr *) &clientname, &size);

        if (new < 0) {
          perror("accept()");
          exit(EXIT_FAILURE);
        }

        printf("Connection established: %s:%hd\n", inet_ntoa(clientname.sin_addr), ntohs(clientname.sin_port));

        // Read from client
        char client_message[MAXMSG];
        recv(new, &client_message, sizeof(client_message), 0);
        printf("==> Received data: '%s'\n", client_message);

        // Send data back to client
        char server_message[MAXMSG];
        sprintf(server_message, "Server received data: '%s'", client_message);
        send(new, server_message, sizeof(server_message), 0);

        FD_SET(new, &write_fds);
      }
    }
  }

  // Close socket
  close(server_socket);
  return 0;
}
