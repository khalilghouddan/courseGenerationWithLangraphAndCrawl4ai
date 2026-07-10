


#import datetime to get the timestamp
from datetime import datetime
#import contextmanager to use it in the log_message function
#context manager start the log befor the servie and end the log after the servie to c   lculate time 
from contextlib import contextmanager

#function that convert hex color code to ANSI code
def hex_to_ansi(hex_color: str) -> str:

    #lstrip remove the # from the hex color code
    hex_color = hex_color.lstrip('#')

    #if the hex color code is 6 digits long
    if len(hex_color) == 6:

        try:
            #convert hex color code to RGB
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"\033[38;2;{r};{g};{b}m"

        except ValueError:
            pass
    #defualt white 
    return "\033[97m"

#function to get timestamp
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

#function to log messages
#this convert normal fuction into context manager

@contextmanager
def log_message(title: str, title_color: str, text: str):

    #we will paste the fiste line here : the start of the seervice 
    #start time
    start_time = datetime.now()
    #convert hex color code to ANSI code
    color_code = hex_to_ansi(title_color)
    #reset color code
    reset_code = "\033[0m"
    #bold color code
    bold_code = "\033[1m"
    #timestamp
    timestamp = get_timestamp()
    #green color for START
    green = hex_to_ansi("#00C853")
    #print start
    print(
        f"\033[97m[{timestamp}]\033[0m "
        f"{color_code}{bold_code}[{title}]{reset_code} "
        f"{green}{bold_code}[START]{reset_code} "
        f"{text}"
    )    
    #now thez second part the end of service 
    #the magic part 
    try:
        #wait until the service is done 
        #yield is where the code inside the with block runs
        #when the code inside the with block finish , it will go to the finally block 
        yield
    finally:
        #calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        #end timestamp
        end_timestamp = get_timestamp()
        #blue color for FINISH
        blue = hex_to_ansi("#448AFF")
        #print finish
    print(
        f"\033[97m[{end_timestamp}]\033[0m "
        f"{color_code}{bold_code}[{title}]{reset_code} "
        f"{blue}{bold_code}[FINISH]{reset_code} "
        f"{text} ({duration:.3f}s)"
    )