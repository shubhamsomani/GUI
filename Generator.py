#Script to generate header file with macro names and their respective values.
# Author : Shubham Somani

import os
from text import text_parser

def create_header(parameters):

    data=open("configuration.ini")
    config_file=data.readlines()
    #data1=open("conf.t")
    #conf_t=data1.readlines()
    #parameters=text_parser.return_parameters(conf_t)

    header_file= open ( 'header.h' , 'w')

    #if(header_file):
    #    print "File opened correctly"
    #else:
    #    print "incorrect"

    final=[]

    # Looping through macro names
    number_of_sections=len(parameters)
    for section_index in xrange(number_of_sections):
        
        for parameter_index in range(1,len(parameters[section_index]),6):
            
            macro_name=parameters[section_index][parameter_index]
            
            if("The default value is " in parameters[section_index][parameter_index+3]):
                temp=parameters[section_index][parameter_index+3].split("The default value is ")
                temp2=temp[1]
                
                if("." in temp2):
                    final=temp2.split(".")
                #CONFIGURE_INIT_TASK_NAME is an exception as its default value has commas in it.
                    
                if("," in temp2 and parameters[section_index][parameter_index]!="CONFIGURE_INIT_TASK_NAME"):
                    final=temp2.split(",")
            elif (parameters[section_index][parameter_index+1]=="Boolean feature macro."):
                final=["FALSE"]
            else:
                final="n/a"

                    
            for config_index in xrange(len(config_file)):
                line=config_file[config_index].upper()
                
                if(macro_name in line):
                    temporary_string=line.split(macro_name)
                    final_value=[]
                    
                    if("=" in temporary_string[1]):
                        final_value=temporary_string[1].split("=")
                        
                        #If user has not entered the same value as that of default value.
                        Value_to_be_compared_1=final_value[1].upper();
                        Value_to_be_compared_2=final[0].upper();
                        if(Value_to_be_compared_1.strip()!=Value_to_be_compared_2.strip()):
                            #Adding Description as a comment
                            if('@code{' in parameters[section_index][parameter_index+4]):
                                #temp=parameters[section_index][parameter_index+4].split('@code{')
                                #temp1=temp[1].split('}')
                                #description=temp[0]+temp1[0]+temp1[1]
                                #header_file.write('\n'+'/*'+description+'*/'+'\n')
                                description=parameters[section_index][parameter_index+4]
                                description=description.replace("@code{","")
                                description=description.replace("}","")
                                header_file.write('\n'+'/*'+description+'*/'+'\n')
                                
                            else:
                                header_file.write('\n'+'/*'+parameters[section_index][parameter_index+4]+'*/'+'\n')
                            #Adding value selected by user.
                            header_file.write('#define '+macro_name+' '+final_value[1].strip()+'\n')
                                
    header_file.close()

#create_header()
