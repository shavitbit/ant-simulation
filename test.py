# Function to calculate square root
def find_square_root(number):
    if number < 0:
        return "Square root is not defined for negative numbers"
    return number ** 0.5

# Example usage
number = 16
square_root = find_square_root(number)
print(f"The square root of {number} is {square_root}")
print(str(16*0.5))