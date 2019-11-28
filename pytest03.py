import random
secret= random.randint(1,20)
print("lalallallallalalalallalalallallala")
temp = input("input a number to guess who am I ??")
guess = int(temp)
while(guess!=secret):
    temp = input("please try again~")
    guess=int(temp)
    if guess == secret:
        print("woc !!!right")
    else:
        if guess>secret:
            print("xixi, wrong ! So big!!!")
        else:
            print("haha, wrong! So small!!!")
print("go away ! bye~")    
