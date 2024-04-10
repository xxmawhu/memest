import hashlib

def unique_12_char_string(input_str):
    # 使用MD5进行哈希计算
    hash_object = hashlib.md5(input_str.encode())
    hex_dig = hash_object.hexdigest()

    # 取前12位作为唯一标识符
    unique_id = hex_dig[:12]

    return unique_id

# 测试
input_str = "This is a long string be hashed."
result = unique_12_char_string(input_str)
print(result)
