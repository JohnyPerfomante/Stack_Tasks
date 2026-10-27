def _visit_range(start, stop, action):
    if start >= stop:
        return
    if stop - start == 1:
        action(start)
        return

    middle = (start + stop) // 2
    _visit_range(start, middle, action)
    _visit_range(middle, stop, action)


# 1. Валідні дужки
def is_valid(s):
    if len(s) % 2 != 0:
        return False

    stack = []
    matching = {")": "(", "]": "[", "}": "{"}
    valid = True

    def inspect(index):
        nonlocal valid
        if not valid:
            return

        bracket = s[index]
        if bracket in "([{":
            stack.append(bracket)
        elif not stack or stack.pop() != matching[bracket]:
            valid = False

    _visit_range(0, len(s), inspect)
    return valid and not stack


# 2. Симетричний обхід дерева: ліве піддерево -> вузол -> праве піддерево
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root):
    values = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        values.append(node.val)
        visit(node.right)

    visit(root)
    return values


# 3. Мінімальний стек: у кожному вузлі зберігаємо мінімум його суфікса
class _MinStackNode:
    def __init__(self, value, minimum, next_node):
        self.value = value
        self.minimum = minimum
        self.next = next_node


class MinStack:
    def __init__(self):
        self._head = None

    def push(self, val):
        minimum = val
        if self._head is not None and self._head.minimum < minimum:
            minimum = self._head.minimum
        self._head = _MinStackNode(val, minimum, self._head)

    def pop(self):
        self._head = self._head.next

    def top(self):
        return self._head.value

    def getMin(self):
        return self._head.minimum


# 4. Черга на двох стеках
class MyQueue:
    def __init__(self):
        self._incoming = []
        self._outgoing = []

    def _prepare_front(self):
        if self._outgoing:
            return

        def transfer_one(_):
            self._outgoing.append(self._incoming.pop())
        _visit_range(0, len(self._incoming), transfer_one)

    def push(self, x):
        self._incoming.append(x)

    def pop(self):
        self._prepare_front()
        return self._outgoing.pop()

    def peek(self):
        self._prepare_front()
        return self._outgoing[-1]

    def empty(self):
        return not self._incoming and not self._outgoing


# 5. Декодування рядка з вкладеними повтореннями k[...]
def decode_string(s):
    def repeat_text(text, count):
        if count == 0:
            return ""
        if count == 1:
            return text

        half = repeat_text(text, count // 2)
        if count % 2 == 0:
            return half + half
        return half + half + text

    def read_number(position, value=0):
        if position == len(s) or not ("0" <= s[position] <= "9"):
            return value, position
        return read_number(position + 1, value * 10 + int(s[position]))

    def parse(position):
        parts = []

        def collect(index):
            if index == len(s) or s[index] == "]":
                return "".join(parts), index

            if "0" <= s[index] <= "9":
                count, opening = read_number(index)
                inner, closing = parse(opening + 1)
                parts.append(repeat_text(inner, count))
                return collect(closing + 1)

            parts.append(s[index])
            return collect(index + 1)

        return collect(position)

    decoded, _ = parse(0)
    return decoded


# 6. Обчислення виразу у зворотній польській нотації
def eval_rpn(tokens):
    stack = []

    def divide_toward_zero(left, right):
        positive_left = -left if left < 0 else left
        positive_right = -right if right < 0 else right
        quotient = positive_left // positive_right
        if (left < 0) != (right < 0):
            return -quotient
        return quotient

    def evaluate(index):
        token = tokens[index]
        if token not in ("+", "-", "*", "/"):
            stack.append(int(token))
            return

        right = stack.pop()
        left = stack.pop()
        if token == "+":
            result = left + right
        elif token == "-":
            result = left - right
        elif token == "*":
            result = left * right
        else:
            result = divide_toward_zero(left, right)
        stack.append(result)

    _visit_range(0, len(tokens), evaluate)
    return stack[-1]


# 7. Довжина найдовшого правильного дужкового підрядка
def longest_valid_parentheses(s):
    stack = [-1]
    longest = 0

    def inspect(index):
        nonlocal longest
        if s[index] == "(":
            stack.append(index)
            return

        stack.pop()
        if not stack:
            stack.append(index)
            return

        length = index - stack[-1]
        if length > longest:
            longest = length

    _visit_range(0, len(s), inspect)
    return longest


if __name__ == "__main__":
    print("1. Валідні дужки:")
    print(is_valid("()"))
    print(is_valid("()[]{}"))
    print(is_valid("(]"))

    print("\n2. Симетричний обхід дерева:")
    example_root = TreeNode(1, None, TreeNode(2, TreeNode(3)))
    print(inorder_traversal(example_root))
    print(inorder_traversal(None))
    print(inorder_traversal(TreeNode(1)))

    print("\n3. Мінімальний стек:")
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print(min_stack.getMin())
    min_stack.pop()
    print(min_stack.top())
    print(min_stack.getMin())

    print("\n4. Черга на двох стеках:")
    queue = MyQueue()
    queue.push(1)
    queue.push(2)
    print(queue.peek())
    print(queue.pop())
    print(queue.empty())

    print("\n5. Декодування рядка:")
    print(decode_string("3[a]2[bc]"))
    print(decode_string("3[a2[c]]"))
    print(decode_string("2[abc]3[cd]ef"))

    print("\n6. Зворотна польська нотація:")
    print(eval_rpn(["2", "1", "+", "3", "*"]))
    print(eval_rpn(["4", "13", "5", "/", "+"]))
    print(eval_rpn([
        "10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+",
    ]))

    print("\n7. Найдовший правильний дужковий підрядок:")
    print(longest_valid_parentheses("(()"))
    print(longest_valid_parentheses(")()())"))
    print(longest_valid_parentheses(""))
