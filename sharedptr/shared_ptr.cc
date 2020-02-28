#include<iostream>
#include<memory>
using namespace std;

class Dog{
    string name;
    public:
        Dog(string got_name){ cout << "Dog is created: " << got_name << endl; name = got_name; }        //* Constructor 1
        Dog(){ cout <<"Nameless dog created." << endl; name = "endless"; }                          //* Constructor 2

        Dog(const Dog &d2){                                         //* Copy Constructor
            cout <<"Running Copy Constructor" << endl;
            name = d2.name;
        }
        ~Dog(){ cout << "Destroyed " << name << endl; }              //* Destructor
        
        void bark(){ cout <<"Dog " << name <<" rules    " << endl; }      //* Some function

};

void foo(){
    Dog *p = new Dog("Draco");
    //....
    delete p;
    //....
    // p->bark();      //* p is a dangling pointer here - undefined behaviour
}                   //* Memory leak can occur if p is not deleted

void foo2(){
    std::shared_ptr<Dog> p(new Dog("Gunner"));      //* Count = 1       // Creating a shared pointer.
    //* 1. "Gunner" is created; 2. p is created.

    {
        shared_ptr<Dog> p2 = p;                     //* Count = 2
        p2->bark();
        cout << p.use_count()<<endl;                      //* 2
    }
    //* p2 gets deleted on its own after its scope ends.
    //* Count = 1
    p-> bark();
}   //* Count = 0


int main(){
    foo();
    foo2();

    //* An object should be assignd to a smart pointer as soon as it is created. Raw pointer should not be used.
    Dog *d = new Dog("Sherry");         //* Bad idea
    shared_ptr<Dog> p(d);               //* p.use_count = 1
    // shared_ptr<Dog> p2(d);              //* p.use_count = 1         // Will result in segmentation fault, since d will be deleted twice.

    shared_ptr<Dog> ptr = make_shared<Dog>("Tank");       //* Faster and Safer 

    (*ptr).bark();
    return 0;
}