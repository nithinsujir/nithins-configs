#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdint.h>

int main(int argc, char **argv)
{
	int fd = open("/dev/mem", O_RDWR);
	uint32_t *map = mmap(NULL, 0xfffff, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

	printf("== [%s@%s:%d]mapped\n", __func__, __FILE__, __LINE__);
	if (fd < 0 || !map) {
		fprintf(stderr, "== [%s@%s:%d]failed\n", __func__, __FILE__, __LINE__);
		return -1;
	}

	printf("== [%s@%s:%d] random value %#x\n", __func__, __FILE__, __LINE__, map[900]);

	return 0;
}

