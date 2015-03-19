#include <stdio.h>
#include <malloc.h>

int main(void)
{
	char *ptr;
	int size = 1000;
	int total = 0;

	while (1) {
		int i;

		ptr = malloc(size * 4 * 1024);

		for (i = 0; i < size; i++)
			ptr[i * 4 * 1024] = i;

		total += size;
		printf("total alloc'd %d\n", total);
		sleep(1);
	}

	return 0;
}

