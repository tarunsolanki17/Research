#include<stdio.h>

float subtract(float in1, float in2)
  {
    float ret = 0.0;
    asm ("fsubr %2, %0" : "=&t" (ret) : "%0" (in1), "u" (in2));
    return ret;
  }

void main(){
	float val;
	val = subtract(5.6,1.4);
	printf("%f",val);

}
