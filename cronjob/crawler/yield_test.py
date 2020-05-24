def myyield():
    print("即将生成2")
    yield 2
    print("即将生成3")
    # return '在生成3之前用return返回'  将会发生异常
    yield 3
    print("即将生成4")
    yield 4
    print("即将生成5")
    yield 5
    print("生成器生成结束")
    yield 
#for x in  myyield():
#    print(x) 
# 调用生成器函数来创建一个生成器,此生成器能生成 2,3,4,5
gen = myyield()
 
it = iter(gen)  #用生成器拿到对应的迭代器
print(next(it)) #此时生成器函数才开始执行,并遇到yield停止 2
print(next(it)) #访问迭代器 3
print(next(it)) #4   
print(next(it)) #5
print(next(it)) #生成器生成结束
