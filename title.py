from termcolor import colored

ascii_art = r"""
 __     __        _                     
 \ \   / /__ _ __| |__  _   _ _ __ ___  
  \ \ / / _ \ '__| '_ \| | | | '_ ` _ \ 
   \ V /  __/ |  | |_) | |_| | | | | | |
    \_/ \___|_|  |_.__/ \__,_|_| |_| |_|
"""

print(colored(ascii_art, "magenta", attrs=["bold"]))