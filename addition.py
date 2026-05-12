#!/usr/bin/env python3
"""
Addition Module

This module provides functions for performing addition operations.
Includes basic addition, multiple number addition, and input validation.
"""

import logging
from typing import Union, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_two_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.
    
    Args:
        a (Union[int, float]): First number
        b (Union[int, float]): Second number
    
    Returns:
        Union[int, float]: Sum of the two numbers
    
    Raises:
        TypeError: If inputs are not numbers
    
    Example:
        >>> add_two_numbers(5, 3)
        8
        >>> add_two_numbers(2.5, 1.5)
        4.0
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers (int or float)")
    
    result = a + b
    logger.info(f"Adding {a} + {b} = {result}")
    return result


def add_multiple_numbers(*numbers: Union[int, float]) -> Union[int, float]:
    """
    Add multiple numbers together.
    
    Args:
        *numbers: Variable number of numeric arguments
    
    Returns:
        Union[int, float]: Sum of all numbers
    
    Raises:
        TypeError: If any input is not a number
        ValueError: If no numbers are provided
    
    Example:
        >>> add_multiple_numbers(1, 2, 3, 4, 5)
        15
        >>> add_multiple_numbers(2.5, 1.5, 3.0)
        7.0
    """
    if not numbers:
        raise ValueError("At least one number must be provided")
    
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All arguments must be numbers, got {type(num).__name__}")
    
    result = sum(numbers)
    logger.info(f"Adding {numbers} = {result}")
    return result


def add_from_list(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Add numbers from a list.
    
    Args:
        numbers (List[Union[int, float]]): List of numbers to add
    
    Returns:
        Union[int, float]: Sum of all numbers in the list
    
    Raises:
        TypeError: If input is not a list or contains non-numeric values
        ValueError: If the list is empty
    
    Example:
        >>> add_from_list([1, 2, 3, 4, 5])
        15
        >>> add_from_list([2.5, 1.5, 3.0])
        7.0
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    if not numbers:
        raise ValueError("List cannot be empty")
    
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All list elements must be numbers, got {type(num).__name__}")
    
    result = sum(numbers)
    logger.info(f"Adding list {numbers} = {result}")
    return result


def safe_add(a: str, b: str) -> Union[int, float, None]:
    """
    Safely add two string representations of numbers.
    
    Args:
        a (str): First number as string
        b (str): Second number as string
    
    Returns:
        Union[int, float, None]: Sum of the numbers or None if conversion fails
    
    Example:
        >>> safe_add("5", "3")
        8
        >>> safe_add("2.5", "1.5")
        4.0
        >>> safe_add("abc", "def")
        None
    """
    try:
        # Try to convert to int first, then float
        try:
            num_a = int(a)
        except ValueError:
            num_a = float(a)
        
        try:
            num_b = int(b)
        except ValueError:
            num_b = float(b)
        
        result = num_a + num_b
        logger.info(f"Safely adding '{a}' + '{b}' = {result}")
        return result
    
    except (ValueError, TypeError) as e:
        logger.error(f"Failed to convert inputs to numbers: {e}")
        return None


def interactive_addition():
    """
    Interactive function to get user input and perform addition.
    """
    print("Welcome to the Addition Calculator!")
    print("Enter 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("Enter first number (or 'quit'): ").strip()
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            second_input = input("Enter second number: ").strip()
            
            result = safe_add(user_input, second_input)
            if result is not None:
                print(f"Result: {user_input} + {second_input} = {result}\n")
            else:
                print("Error: Please enter valid numbers.\n")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    # Example usage
    print("Addition Module Examples:")
    print("========================")
    
    # Basic addition
    print(f"add_two_numbers(5, 3) = {add_two_numbers(5, 3)}")
    print(f"add_two_numbers(2.5, 1.5) = {add_two_numbers(2.5, 1.5)}")
    
    # Multiple numbers
    print(f"add_multiple_numbers(1, 2, 3, 4, 5) = {add_multiple_numbers(1, 2, 3, 4, 5)}")
    
    # From list
    print(f"add_from_list([10, 20, 30]) = {add_from_list([10, 20, 30])}")
    
    # Safe addition
    print(f"safe_add('15', '25') = {safe_add('15', '25')}")
    print(f"safe_add('abc', 'def') = {safe_add('abc', 'def')}")
    
    print("\n")
    
    # Run interactive mode
    interactive_addition()