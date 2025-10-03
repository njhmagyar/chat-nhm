"""Fix for OpenAI client proxies issue"""

import openai

# Store the original __init__ method
_original_openai_init = openai.OpenAI.__init__

def fixed_openai_init(self, *args, **kwargs):
    """Fixed OpenAI.__init__ that removes problematic arguments"""
    # Remove arguments that cause issues
    problematic_args = ['proxies', 'http_client']
    for arg in problematic_args:
        if arg in kwargs:
            kwargs.pop(arg)
    
    return _original_openai_init(self, *args, **kwargs)

# Apply the fix
openai.OpenAI.__init__ = fixed_openai_init