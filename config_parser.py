from text import text_parser
import ConfigParser

index=0

#function to write data into .ini file
def write():

    #using python's config parser
    config=ConfigParser.RawConfigParser()
    
    #getting data from text parser
    parameters=text_parser.return_parameters()

    global index

    number_of_sections=len(parameters)
    section_name="start"
    config.add_section(section_name)
    
    for section_index in xrange(number_of_sections):
        config.set(section_name,str(index),'start of section')
        index=index+1
        config.set(section_name,str(index),parameters[section_index][0])
        index=index+1
        
        for parameter_index in range(1,len(parameters[section_index]),1):
            config.set(section_name,str(index),parameters[section_index][parameter_index])
            index=index+1

    #writing into configuration.ini 
    with open('configuration.ini','wb') as configfile:
        config.write(configfile)


#--------------------------------------------------------------------------------------------------
        
#function to read from .ini file
def read():
    parameters=[]
    global index
    config=ConfigParser.RawConfigParser()

    config.read('configuration.ini')
    section_name="start"
    section_index=-1
    parameter_index=0
    
    for i in xrange(index):
        temp=config.get(section_name,str(i))
        
        if(temp=='start of section'):
            section_index=section_index+1
            parameters.append([])
            continue
        
        parameters[section_index].append(temp)

    #print parameters
    return parameters

#write()
#read()
