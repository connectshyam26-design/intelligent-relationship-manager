from app.tools import get_customer_profile


class FakeToolContext:
    def __init__(self):
        self.state = {}


context = FakeToolContext()

print("Initial state:")
print(context.state)

print("\nLoading C123...")
result1 = get_customer_profile(
    customer_id="C123",
    tool_context=context,
)

print("Customer:")
print(result1)

print("Session state:")
print(context.state)

print("\nLoading C456...")
result2 = get_customer_profile(
    customer_id="C456",
    tool_context=context,
)

print("Customer:")
print(result2)

print("Session state:")
print(context.state)