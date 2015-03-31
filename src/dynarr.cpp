#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	int x = atoi(argv[1]);
	long arr[x];

	printf("size %lu\n", sizeof(arr));
	
	return 0;
}

