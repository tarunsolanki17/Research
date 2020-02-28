#include <iostream>
extern int global_flag;
extern void change_global();


int main()
{
    change_global();
    if(global_flag==1){
        printf("Yess value = %d",global_flag);
    }
    return 0;
}
