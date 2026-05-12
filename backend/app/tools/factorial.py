"""
Factorial Implementation Module

This module provides multiple implementations of factorial calculation
with different approaches for educational and performance comparison purposes.

Author: AI Assistant
Date: 2026-05-12
"""

import math
from functools import lru_cache
from typing import Union


class FactorialCalculator:
    """
    A comprehensive factorial calculator with multiple implementation approaches.
    """

    @staticmethod
    def factorial_iterative(n: int) -> int:
        """
        Calculate factorial using iterative approach.
        
        Args:
            n (int): Non-negative integer to calculate factorial for
            
        Returns:
            int: Factorial of n
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
            
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        
        return result

    @staticmethod
    def factorial_recursive(n: int) -> int:
        """
        Calculate factorial using recursive approach.
        
        Args:
            n (int): Non-negative integer to calculate factorial for
            
        Returns:
            int: Factorial of n
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
            RecursionError: If n is too large (exceeds recursion limit)
            
        Time Complexity: O(n)
        Space Complexity: O(n) due to call stack
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        # Base cases
        if n == 0 or n == 1:
            return 1
        
        # Recursive case
        return n * FactorialCalculator.factorial_recursive(n - 1)

    @staticmethod
    @lru_cache(maxsize=128)
    def factorial_memoized(n: int) -> int:
        """
        Calculate factorial using memoization for performance optimization.
        
        Args:
            n (int): Non-negative integer to calculate factorial for
            
        Returns:
            int: Factorial of n
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
            
        Time Complexity: O(n) for first call, O(1) for subsequent calls
        Space Complexity: O(n) for memoization cache
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if n == 0 or n == 1:
            return 1
        
        return n * FactorialCalculator.factorial_memoized(n - 1)

    @staticmethod
    def factorial_builtin(n: int) -> int:
        """
        Calculate factorial using Python's built-in math.factorial function.
        
        Args:
            n (int): Non-negative integer to calculate factorial for
            
        Returns:
            int: Factorial of n
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
            
        Time Complexity: O(n) - optimized C implementation
        Space Complexity: O(1)
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")
        
        return math.factorial(n)

    @staticmethod
    def factorial_tail_recursive(n: int, accumulator: int = 1) -> int:
        """
        Calculate factorial using tail recursion optimization.
        
        Args:
            n (int): Non-negative integer to calculate factorial for
            accumulator (int): Accumulator for tail recursion
            
        Returns:
            int: Factorial of n
            
        Raises:
            ValueError: If n is negative
            TypeError: If n is not an integer
            
        Time Complexity: O(n)
        Space Complexity: O(n) - Python doesn't optimize tail recursion
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected integer, got {type(n).__name__}")
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if n == 0 or n == 1:
            return accumulator
        
        return FactorialCalculator.factorial_tail_recursive(n - 1, n * accumulator)


def factorial(n: Union[int, str], method: str = "iterative") -> int:
    """
    Convenient wrapper function for factorial calculation.
    
    Args:
        n (Union[int, str]): Number to calculate factorial for
        method (str): Method to use ('iterative', 'recursive', 'memoized', 'builtin', 'tail_recursive')
        
    Returns:
        int: Factorial of n
        
    Raises:
        ValueError: If method is not supported or n is invalid
        
    Examples:
        >>> factorial(5)
        120
        >>> factorial("5", "recursive")
        120
        >>> factorial(0)
        1
    """
    # Convert string to int if needed
    if isinstance(n, str):
        try:
            n = int(n)
        except ValueError:
            raise ValueError(f"Cannot convert '{n}' to integer")
    
    calculator = FactorialCalculator()
    
    methods = {
        "iterative": calculator.factorial_iterative,
        "recursive": calculator.factorial_recursive,
        "memoized": calculator.factorial_memoized,
        "builtin": calculator.factorial_builtin,
        "tail_recursive": calculator.factorial_tail_recursive
    }
    
    if method not in methods:
        raise ValueError(f"Unsupported method '{method}'. Available: {list(methods.keys())}")
    
    return methods[method](n)


def factorial_range(start: int, end: int, method: str = "iterative") -> dict:
    """
    Calculate factorials for a range of numbers.
    
    Args:
        start (int): Starting number (inclusive)
        end (int): Ending number (inclusive)
        method (str): Method to use for calculation
        
    Returns:
        dict: Dictionary mapping numbers to their factorials
        
    Examples:
        >>> factorial_range(1, 5)
        {1: 1, 2: 2, 3: 6, 4: 24, 5: 120}
    """
    if start < 0 or end < 0:
        raise ValueError("Range values must be non-negative")
    
    if start > end:
        start, end = end, start
    
    return {i: factorial(i, method) for i in range(start, end + 1)}


def is_factorial(n: int) -> tuple[bool, int]:
    """
    Check if a number is a factorial of some integer.
    
    Args:
        n (int): Number to check
        
    Returns:
        tuple[bool, int]: (is_factorial, base_number) or (False, -1)
        
    Examples:
        >>> is_factorial(120)
        (True, 5)
        >>> is_factorial(100)
        (False, -1)
    """
    if n < 1:
        return False, -1
    
    if n == 1:
        return True, 0  # 0! = 1 and 1! = 1
    
    current = 1
    i = 1
    
    while current < n:
        i += 1
        current *= i
    
    return (current == n, i if current == n else -1)


if __name__ == "__main__":
    # Demo and testing
    print("=== Factorial Calculator Demo ===")
    
    test_numbers = [0, 1, 5, 10, 15]
    methods = ["iterative", "recursive", "memoized", "builtin", "tail_recursive"]
    
    for num in test_numbers:
        print(f"\nFactorial of {num}:")
        for method in methods:
            try:
                result = factorial(num, method)
                print(f"  {method:15}: {result}")
            except Exception as e:
                print(f"  {method:15}: Error - {e}")
    
    # Range calculation demo
    print("\n=== Factorial Range (1-10) ===")
    range_result = factorial_range(1, 10)
    for num, fact in range_result.items():
        print(f"{num}! = {fact}")
    
    # Factorial check demo
    print("\n=== Factorial Check Demo ===")
    test_values = [1, 6, 24, 120, 100, 720]
    for val in test_values:
        is_fact, base = is_factorial(val)
        if is_fact:
            print(f"{val} is {base}!")
        else:
            print(f"{val} is not a factorial")