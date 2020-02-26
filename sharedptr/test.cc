#include <iostream>
#include <memory>

struct A {
    int x;
    A(int y) : x(y)
    {
        std::cout << "constructor for A" << std::endl;
    }
    A(const A& copy) : x(copy.x)
    {
        std::cout << "copy-constructor for A" << std::endl;
    }
    ~A()
    {
        std::cout << "destructor for A" << std::endl;
    }
};

A foo(A& b)
{
    A c(b.x+1);
    return c;
}

int main()
{
    //std::shared_ptr<A> a = std::make_shared<A>(33);
    //std::cout << "a = " << a->x << std::endl;
    A a(4);
    A b = foo(a);
    std::cout << "b = " << b.x << std::endl;
    return 0;
}
