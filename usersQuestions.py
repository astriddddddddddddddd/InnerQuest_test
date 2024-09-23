# 初始化一個空的使用者數組，每個使用者都有一個字符串數組
users_question_arrays = {}

# 函數：新增或更新使用者的字符串數組
def add_user_question(username, new_question):
    if username not in users_question_arrays:
        users_question_arrays[username] = []
    users_question_arrays[username].append(new_question)
    print(f"'{new_question}' 已新增到使用者 '{username}' 的數組中。")

# 函數：刪除特定使用者的字符串數組
def delete_user_question(username, question_to_delete):
    if username in users_question_arrays:
        if question_to_delete in users_question_arrays[username]:
            users_question_arrays[username].remove(question_to_delete)
            print(f"'{question_to_delete}' 已從使用者 '{username}' 的數組中刪除。")
        else:
            print(f"字串 '{question_to_delete}' 不存在於使用者 '{username}' 的數組中。")
    else:
        print(f"使用者 '{username}' 不存在。")
        
# 函數：刪除特定使用者的所有字符串數組
def clear_user_questions(username):
    if username in users_question_arrays:
        users_question_arrays[username] = []
        print(f"使用者 '{username}' 的所有字符串數組已被清空。")
    else:
        print(f"使用者 '{username}' 不存在。")
        
# 函數：刪除特定使用者的最後一個字符串數組
def delete_last_user_question(username):
    if username in users_question_arrays:
        if users_question_arrays[username]:
            last_string = users_question_arrays[username].pop()
            print(f"使用者 '{username}' 的最後一個字串 '{last_string}' 已被刪除。")
        else:
            print(f"使用者 '{username}' 的字符串數組是空的。")
    else:
        print(f"使用者 '{username}' 不存在。")
        
# 函數：刪除特定使用者的最後一個字符串數組
def return_last_user_question(username):
    if username in users_question_arrays:
        if users_question_arrays[username]:
            return users_question_arrays[username][-1]  # 回傳最後一個字串           
        else:
            print(f"使用者 '{username}' 的字符串數組是空的。")
    else:
        print(f"使用者 '{username}' 不存在。")
        
# 函數：返回特定使用者的字符串數組數量
def get_user_question_count(username):
    if username in users_question_arrays:
        count = len(users_question_arrays[username])
        print(f"使用者 '{username}' 的字符串數組中有 {count} 個字串。")
        return count
    else:
        print(f"使用者 '{username}' 不存在。")
        return 0

# 函數：新增使用者
def add_user(username):
    if username not in users_question_arrays:
        users_question_arrays[username] = []
        print(f"使用者 '{username}' 已新增。")
    else:
        print(f"使用者 '{username}' 已經存在。")

# 函數：刪除使用者
def delete_user(username):
    if username in users_question_arrays:
        del users_question_arrays[username]
        print(f"使用者 '{username}' 及其所有字符串數組已刪除。")
    else:
        print(f"使用者 '{username}' 不存在。")
        
# 函數：回傳特定使用者的所有字串
def return_user_questions(username):
    rsp = ""
    if username in users_question_arrays:
        print(f"使用者 '{username}' 的所有字串如下：")
        for idx, s in enumerate(users_question_arrays[username]):
            print(f"{idx + 1}: {s}")
            rsp = rsp + s
    else:
        print(f"使用者 '{username}' 不存在。")        
    return rsp
    
# 函數：打印特定使用者的所有字串
def print_user_questions(username):
    if username in users_question_arrays:
        print(f"使用者 '{username}' 的所有字串如下：")
        for idx, s in enumerate(users_question_arrays[username]):
            print(f"{idx + 1}: {s}")
    else:
        print(f"使用者 '{username}' 不存在。")

# 函數：打印所有使用者的所有字串
def print_all_users_questions():
    if users_question_arrays:
        for username, questions in users_question_arrays.items():
            print(f"\n使用者 '{username}' 的所有字串如下：")
            for idx, s in enumerate(questions):
                print(f"{idx + 1}: {s}")
    else:
        print("沒有任何使用者。")

# 測試這些函數
'''
add_user("user1")
add_user("user2")

add_user_question("user1", "Hello")
add_user_question("user1", "World")
add_user_question("user2", "Python")
add_user_question("user2", "Programming")

print_user_questions("user1")  # 打印 user1 的所有字串
print_user_questions("user2")  # 打印 user2 的所有字串
print(return_user_questions("user1")) # return user1 的所有字串
print(return_user_questions("user2")) #return user1 的所有字串

delete_user_question("user1", "Hello")  # 從 user1 刪除 "Hello"

print_user_questions("user1")  # 再次打印 user1 的所有字串

print_all_users_questions()  # 打印所有使用者的所有字串

delete_user("user1")  # 刪除使用者 user1

print_all_users_questions()  # 再次打印所有使用者的所有字串

add_user("user1")
add_user_question("user1", "你是否覺得世界與你隔絕，讓你感到寒冷且無力？Yes.")
add_user_question("user1", "你是否覺得自己像個局外人，觀察著這個世界，卻無法融入其中？Yes.")
add_user_question("user1", "你是否渴望與他人建立連結，卻感到無能為力？Yes")
add_user_question("user1", "你是否經常感到焦慮或抑鬱？Yes")
print(return_user_questions("user1")) # return user1 的所有字串
clear_user_questions("user1")
print(return_user_questions("user1")) # return user1 的所有字串
print("End Test")
'''