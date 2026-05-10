# 認識裝飾詞(Decorator)的用法
# ===================================
# 第一段:函式可以當作參數傳遞給另一個函式


# ===================================
def say_hello():
    print("Hello")


def run_with_announce(func):
    print("* 準備執行...")
    func()
    print("* 執行完畢!")


print("直接呼叫:")
say_hello()

print()
print("透過 run_with_announce 呼叫:")
run_with_announce(say_hello)


def gift_wrap(func):
    def wrapper():
        print("_____前置動作_____")
        func()
        print("_____後製動作_____")

    return wrapper


def say_hello():
    print("Hello!")


say_hello = gift_wrap(say_hello)

say_hello()

print("-------------------------")


@gift_wrap
def say_hello():
    print("Hello!")


say_hello()

print()
print(">>>連結 Discord Bot:")
print(">>>@bot.event 就是這種用法")
print(">>>Discord 幫你定義好bot.event 這個裝飾詞")
print(">>>在函式上加 @bot.,event，Discord 就知道這個函式是事件處理器")

print("--------------------------")


def register_command(name, description):
    print(f"[登記]指令 /{name}:{description}")

    def decorator(func):
        def wrapper():
            print(f"[執行]指令 /{name}")
            func()

        return wrapper

    return decorator


@register_command("hello", description="打招呼")
def hello_command():
    print("你好!我是 hello指令!")


hello_command()
print("---------------------------")
