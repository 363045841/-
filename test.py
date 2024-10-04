add = [1, 2, 3]  # 假设这是你的数组

# 如果数组的长度小于15，扩展它
while len(add) < 15:
    add.append(None)  # 或者你想要的默认值

# 在第15项（索引14）插入元素
add[14] = "new_element"

print(add)
