

#helper functions
#convert type to pascal
def type_to_pascal(type):
    words = type.split('_')
    output_string =''
    for word in words:
        if(word in ['PH','AC','DC']):
            output_string=output_string+word
        else:
            output_string=output_string+word.title()
    return output_string