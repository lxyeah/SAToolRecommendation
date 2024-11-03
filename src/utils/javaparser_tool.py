import javalang
import re

def find_matching_bracket(lines, start_line):
    open_brackets = 0
    in_block_comment = False

    bracket_start_line = start_line
    for line_num, line in enumerate(lines[start_line:], start=start_line):
        # 跳过行注释
        line = re.sub(r'//.*', '', line)

        # 处理块注释
        block_comment_start = line.find('/*')
        block_comment_end = line.find('*/')

        if not in_block_comment and block_comment_start != -1:
            in_block_comment = True
            line = line[:block_comment_start]

        if in_block_comment and block_comment_end != -1:
            in_block_comment = False
            line = line[block_comment_end + 2:]

        if in_block_comment:
            bracket_start_line += 1
            continue

        if '{' in line:
            break

        bracket_start_line += 1

    for line_num, line in enumerate(lines[bracket_start_line:], start=bracket_start_line):
        # 跳过行注释
        line = re.sub(r'//.*', '', line)

        # 处理块注释
        block_comment_start = line.find('/*')
        block_comment_end = line.find('*/')

        if not in_block_comment and block_comment_start != -1:
            in_block_comment = True
            line = line[:block_comment_start]

        if in_block_comment and block_comment_end != -1:
            in_block_comment = False
            line = line[block_comment_end + 2:]

        if in_block_comment:
            continue

        open_brackets += line.count('{') - line.count('}')
        if open_brackets == 0:
            return line_num
    return None


def find_method_of_line(java_path, target_line):
    with open(java_path, 'r') as f:
        java_code = f.read()
    f.close()

    tree = javalang.parse.parse(java_code)
    lines = java_code.split('\n')

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        method_name = node.name
        method_start_line = node.position.line
        open_lines = find_matching_bracket(lines, method_start_line - 1)
        if open_lines is None:
            continue

        method_end_line = find_matching_bracket(lines, method_start_line - 1) + 1

        if method_start_line and method_end_line:
            if int(method_start_line) <= int(target_line) <= int(method_end_line):
                return method_name
    # print(f"The line {target_line} doesn't belong to any method.")
    return None


# 示例Java代码
# java_code = """
# public class HelloWorld {
#     public static void main(String[] args) {
#         // This is a { comment
#         System.out.println("Hello, World!");}
#
#     public void test() {
#         // {
#         int a = 6;
#         int b = 4;}
# }
# """

# 设定目标行
# target_line = 2

# with open('PortFinder.java', 'r') as f:
#     content = f.read()
# f.close()

# 调用函数并打印结果
# result = find_method_of_line('PortFinder.java', target_line)
# print(result)
