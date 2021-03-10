# A sample C code
```C

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

```

# A sample call graph
< Functions > ->: g{int ()} f{int ()} 

f ->: g{int ()} funcPtr{int (*)()} < >{float (*)()} 

g ->: externFunc{int ()}

- 说明：
  - 第一行<Functions >后面是当前C文件中定义的函数的汇总。这些函数在后面都会有一行信息，表示其调用的函数。
  - 如果调用的函数没有对应的符号名（比如函数指针数组的引用, funcArr[i]())，则输出<>后面接函数类型。