#!/usr/bin/env python3
'''
Async Comprehensions
'''

import asyncio
import random
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    ''' Creates a list of 10 numbers from a 10-number generator '''
    return [i async for i in async_generator()]
