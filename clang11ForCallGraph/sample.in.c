int (*funcPtr)();
float (*funcArr[])();

int externFunc();
int g(){ externFunc(); }
int f()
{
    int i;
    funcPtr = externFunc;

    g();
    //externFunc();
    funcPtr();
    funcArr[i]();

  return 0;
}

