#include <stdio.h>
#include <stdlib.h>

float subtract(float in1, float in2)
{
  float ret = 0.0;
  asm ("fsubr %2, %0" : "=&t" (ret) : "%0" (in1), "u" (in2));
  return ret;
}

int main(int argc, char* argv[]) {
  if(argc != 3) {
    printf("syntax errror. need two arguments.\n");
    return 1;
  }

  double f1 = atof(argv[1]);
  double f2 = atof(argv[2]);
  double r = subtract(f1, f2);
  printf("%f\n", r);
}
