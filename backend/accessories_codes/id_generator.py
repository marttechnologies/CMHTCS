from backend.db_models.mini_models import IDTracker 
from string import ascii_uppercase, digits
import math
# Generates ID SEQUENTIALLY
from backend.db_models.mini_models import IDTracker 

def number_to_letters(n, length=3):
    """Convert a number to an n-letter uppercase code using base-26"""
    letters = ascii_uppercase
    result = ''
    
    for _ in range(length):
        n, remainder = divmod(n, 26)
        result = letters[remainder] + result

    return result

def id_gen(number_of_letters=2,
           number_of_numbers=4,
           staff=False,
           guardian=False,
           force_change_number_of_numbers=False):
    """
    Generate User ID Based on sequence of letters and numbers sequentially.
    it follow that when the next ID is requested the function retrieves the last ID from IDTracker model
    and increments it by one. then it calculates the new ID based on the last ID.
    
    AA0000 -> AA0001 -> AA0002 -> AA0003 ...
    
    for staff it makes the number of numbers 2 making it 4 DIgit ID By default 
    for staff it makes the number of numbers 3 making it 5 DIgit ID By default 
    
    NB: The process is not random, it is sequential.
    """
    
    if staff:
        number_of_numbers = 2 if not force_change_number_of_numbers else number_of_numbers
    elif guardian:
        number_of_numbers = 3 if not force_change_number_of_numbers else number_of_numbers
    
    # Retrieve the last index from IDTracker
    try:
        if staff:
            id_object = IDTracker.objects.get(user_type='staff')
            last_id = IDTracker.objects.get(user_type='staff').last_id
        elif guardian:
            id_object = IDTracker.objects.get(user_type='staff')
            last_id = IDTracker.objects.get(user_type='guardian').last_id
        else:
            id_object = IDTracker.objects.get(user_type='staff')
            last_id = IDTracker.objects.get(user_type='student').last_id
    except IDTracker.DoesNotExist:
        last_id = 0
        if staff:
            id_object = IDTracker.objects.get(user_type='staff')
            IDTracker.objects.create(user_type='staff', last_id=last_id)
        elif guardian:
            id_object = IDTracker.objects.get(user_type='staff')
            IDTracker.objects.create(user_type='guardian', last_id=last_id)
        else:
            id_object = IDTracker.objects.get(user_type='staff')
            IDTracker.objects.create(user_type='student', last_id=last_id)
        
        
    # Update the IDTracker with the next ID for the next call
    next_id = last_id + 1
    id_object.last_id = next_id
    id_object.save()
    
    # Generate the ID
    full_id = str(last_id).zfill(number_of_numbers + number_of_letters)
    
    number_part = full_id[number_of_letters:]
    
    nth_letters = int(full_id[:number_of_letters])
    letter_part = number_to_letters(nth_letters, length=number_of_letters)
    
    
    return letter_part + number_part
    
    
    