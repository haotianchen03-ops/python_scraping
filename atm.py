account = 0
def balance(name):
    global account
    print(f"您的余额剩余{account}")


def deposit(name):
    global account
    x = int(input("您想存多少"))
    account = account + x
    print(f"您好，您存款{x}成功")
    balance(account)


def withdraw(name):
    global account
    x = int(input("您想取多少"))
    if x > account:
        print("余额不足")
    else:
        account = account - x
        print(f"您好，您已取出{x}")
        balance(account)

choice = 0
name = input("名称\n")
while choice != 4:
    choice = int(input("您好，请选择您想要的操作:\n1:查询余额\n2:存款\n3:取款\n4:退出\n"))
    if choice == 1:
        balance(name)
    elif choice == 2:
        deposit(name)
    elif choice == 3:
        withdraw(name)
