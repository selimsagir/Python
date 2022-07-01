#include<iostream>
#include<stdio.h>
#include<fstream>
#include<string>
#include<math.h>
#include<cstdlib>
//#include "RND.H"

//Constansts
#define pi 3.14765

int a,b,i,j;
float p[100],k[100] ;

using namespace std;

int main(){


/*
fstream fout;

fout.open("foo.csv",ios::out |ios::app);

 std::ifstream f("foo.cvs");
 ifstream foo;
*/
 ofstream foo ("foo.csv");

long int seed;
seed=-5;
rand(&seed);
seed=14;

for ( i = 0; i < 50; i++)
{
    
   
   p[i]=sin(i)*pi*rand(&seed);
   /*
    csvfile<< p[i];
    csvfile <<k[i];
    */
   foo<<p<<endl;

}




foo.close();



return 0;
    
}