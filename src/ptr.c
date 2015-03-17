#include <stdio.h>
#include <stdint.h>

struct fw_hdr {
	uint32_t version;
	uint32_t base_addr;
	uint32_t len;
};

int main(void)
{
	struct fw_hdr *fh = 0;

	printf("== [%s@%s:%d] fh + 1 %p\n", __func__, __FILE__, __LINE__, fh + 1);
	printf("== [%s@%s:%d] (void *) fh + 1 %p\n", __func__, __FILE__, __LINE__, (void*)fh + 1);
	return 0;
}

