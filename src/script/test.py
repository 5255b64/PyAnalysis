

def run():
    def inner_fun1():
        print("inner_fun1 x1="+x1)
    def inner_fun2():
        print("inner_fun1 x2="+x2)

    x1 = "123"
    x2 = "456"
    inner_fun1()
    inner_fun2()



if __name__ == "__main__":
    run()
