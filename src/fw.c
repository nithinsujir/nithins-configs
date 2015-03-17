#include <stdio.h>

typedef unsigned int u32;

static const u32 tg3_57766_fwdata[] = {
0x00000000, 0, 0, 0,
(u32)0, (u32)0,
0x27800001, 0xf7f0403e, 0xcd283674, 0x11001100,
0xf7ff1064, 0x376e0001, 0x27600000, 0xf7f07fea,
0xf7f00004, 0xf7f00018, 0xcc10362c, 0x00180018,
0x17800000, 0xf7f00008, 0xc33836b0, 0xf7f00004,
0xc43836b0, 0xc62036bc, 0x00000009, 0xcb3836b0,
0x17800001, 0x1760000a,
(u32)0, (u32)0,
0xd044d816,
(u32)0, (u32)0,
0x02300202,
};


int main()
{
	printf("== [%s@%s:%d] %x\n", __func__, __FILE__, __LINE__, sizeof(tg3_57766_fwdata));

	return 0;
}

