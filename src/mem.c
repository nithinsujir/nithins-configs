#include <stdio.h>
#include <malloc.h>
#include <unistd.h>

int main(void)
{
	volatile char *ptr;
	int pages = 10;
	int tot_pages = 0;

	while (1) {
		int i;

		ptr = malloc(pages * 4096);
		if (!ptr)
			printf("malloc failed\n");

		for (i = 0; i < pages; i++)
			ptr[i * 4096] = i;

		tot_pages += pages;

		usleep(100);
	}
}

