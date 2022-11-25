s = "salman*1*3"
s_list = s.split("*")
# e.g s_list = ['salman', '1']

j = 0
real_string = ""
for i in s_list:
    if i.isdigit():
        for i in s_list[j:]:
            real_string += i + "*"
            print(real_string)

        # real_string = "".join(s_list[j:])
        # print(real_string)

        break
    j += 1
text = real_string[:-1]


if __name__ == '__main__':

    print(text)