#include <iostream>
#include "header.h"

namespace myns {
    void foo() {
    set_global();
    std::cout << global << std::endl;
    }
}
int main()
{
    myns::foo();
    return 0;
}
