#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <pthread.h>
 
#ifndef MAXMSG
#define MAXMSG 256
#endif

pthread_mutex_t lock;
static const char *LOGFILE = "socket.log";
int NUM_MESSAGES = 30;
static const char* const MESSAGES[] = {
  "Where do random thoughts come from?", "A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.", "The lake is a long way from here.", "Joe made the sugar cookies; Susan decorated them.", "They got there early, and they got really good seats.",
  "Cats are good pets, for they are clean and are not noisy.", "The mysterious diary records the voice.", "I am never at home on Sundays.", "My Mum tries to be cool by saying that she likes all the same things that I do.", "How was the math test?",
  "He turned in the research paper on Friday; otherwise, he would have not passed the class.", "It was getting dark, and we weren’t there yet.", "She did not cheat on the test, for it was not the right thing to do.", "There was no ice cream in the freezer, nor did they have money to go to the store.", "She wrote him a long letter, but he didn't read it.",
  "She always speaks to him in a loud voice.", "I currently have 4 windows open up… and I don’t know why.", "If Purple People Eaters are real… where do they find purple people to eat?", "He told us a very exciting adventure story.", "Everyone was busy, so I went to the movie alone.",
  "A glittering gem is not enough.", "The old apple revels in its authority.", "Wow, does that work?", "This is the last random sentence I will be writing and I am going to stop mid-sent", "She borrowed the book from him many years ago and hasn't yet returned it.",
  "I would have gotten the promotion, but my attendance wasn’t good enough.", "This is a Japanese doll.", "The clock within this blog and the clock on my laptop are 1 hour different from each other.", "The memory we used to share is no longer coherent.", "Italy is my favorite country; in fact, I plan to spend two weeks there next year."
};


struct arg_struct {
  char server_ip[MAXMSG];
  int server_port;
  char log_file[MAXMSG];
};


void *connect_to_server(void *arguments) {
  struct arg_struct *args = arguments;
  // Create socket
  int network_socket;
  network_socket = socket(AF_INET, SOCK_STREAM, 0);

  // Address for socket
  struct sockaddr_in server_address;
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(args->server_port); // specify port
  server_address.sin_addr.s_addr = inet_addr(args->server_ip); // specify IP address
  // Connect to server
  int connection_status;
  connection_status = connect(network_socket, (struct sockaddr *) &server_address, sizeof(server_address));
  // Check connection
  if (connection_status < 0) {
    perror("Connection failed");
    exit(EXIT_FAILURE);
  }
  // Send data
  char client_message[MAXMSG];
  strcpy(client_message, MESSAGES[rand() % NUM_MESSAGES]);
  send(network_socket, client_message, sizeof(client_message), 0);
  // Receive data from server
  char server_response[MAXMSG];
  recv(network_socket, &server_response, sizeof(server_response), 0);
  // Output data; use lock to prevent corruption
  pthread_mutex_lock(&lock); // lock file
  FILE *fp;
  fp = fopen(args->log_file, "a");
  fprintf(fp, "%s\n", server_response);
  fclose(fp);
  pthread_mutex_unlock(&lock); // unlock file
  // Close socket
  close(network_socket);
  // Exit thread
  pthread_exit(NULL);
}


int main(int argc, char const *argv[]) {
  // Takes in 3 arguments:
  //    <IP address of server>
  //    <Port number of server>
  //    <number of clients (threads) to start concurrently>
  if (argc != 4) {
    printf("Usage: %s <server IP> <server port> <number of clients>\n", argv[0]);
    return 1;
  }
  // Parse input
  const char *server_ip = argv[1];
  int server_port = atoi(argv[2]);
  int num_clients = atoi(argv[3]);

  // Generate seed for rand()
  srand(time(NULL));

  // Create mutex lock
  if (pthread_mutex_init(&lock, NULL) != 0) {
    perror("Mutex init");
    exit(EXIT_FAILURE);
  }

  // Create threads
  pthread_t threads[num_clients];
  struct arg_struct args;
  strcpy(args.server_ip, server_ip);
  args.server_port = server_port;
  strcpy(args.log_file, LOGFILE);

  for (int i=0; i<num_clients; i++) {
    if (pthread_create(&threads[i], NULL, connect_to_server, (void *)&args) != 0) {
      perror("Thread creation");
      exit(EXIT_FAILURE);
    }
  }

  // Wait for threads to terminate
  for (int i=0; i<num_clients; i++) {
    pthread_join(threads[i], NULL);
  }

  // Destroy lock
  pthread_mutex_destroy(&lock);

  return 0;
}
