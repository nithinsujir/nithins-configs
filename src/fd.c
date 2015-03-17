#include <stdio.h>
#include <fcntl.h>

int main(int argc, char **argv) {
	int fd1 = open("/tmp/a", O_RDWR);
	int fd2 = open("/tmp/b", O_RDWR);
	int fd3 = open("/tmp/c", O_RDWR);

	printf("== [%s@%s:%d] %d %d %d\n", __func__, __FILE__, __LINE__, fd1, fd2, fd3);

	close(fd2);

	fd2 = open("/tmp/d", O_RDWR);
	printf("== [%s@%s:%d] %d %d %d\n", __func__, __FILE__, __LINE__, fd1, fd2, fd3);

	return 0;
}


