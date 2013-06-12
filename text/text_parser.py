# A text parser which operates on conf.t
# Author : Shubham Somani

def return_parameters():
    
    #-----------section on parsing from the conf.t file---------------------

    data=open("conf.t")
    contents=data.readlines()

    # Variable Declarations
    list=[]
    count_of_sections=0
    start=0

    for index in range(0,len(contents)):
        if "@section" in contents[index]:               
            s=contents[index].split("@section")
            if s[1].strip()=="Classic API Configuration":
                start=1
        if "@section" in contents[index] and start==1:               
            s=contents[index].split("@section")
            #print s[1].strip()
            if count_of_sections>0:
                list.append("end of subsection")
            list.append(s[1].strip())
            count_of_sections=count_of_sections+1

        # Parsing the name of the parameter
        if "@findex" in contents[index] and count_of_sections>0:
            s=contents[index].split("@findex")
            list.append(s[1].strip())
            while(contents[index].strip()!="@end table"):
                index=index+1

                # Data type
                if(contents[index].strip()=="@item DATA TYPE:"):
                    #print contents[index+1]
                    list.append(contents[index+1].strip())

                # Range
                if(contents[index].strip()=="@item RANGE:"):
                    list.append(contents[index+1].strip())

                # Default Value
                if(contents[index].strip()=="@item DEFAULT VALUE:"):
                    input_string=""
                    index=index+1
                    while(contents[index].strip()!="@end table"):
                        input_string=input_string+" "+contents[index].strip()
                        index=index+1
                    if("@code{" in input_string):
                        string=input_string.split("@code{")
                        temp=string[0]+string[1]
                        temp2=temp.split("}")
                        string_after_operations=temp2[0]+" "+temp2[1]
                        list.append(string_after_operations)
                    else:
                        list.append(input_string)
 
            # Description  
            while (contents[index].strip()!="@subheading DESCRIPTION:"):
                index=index+1

            description=""
            index=index+1
            while(contents[index].strip()!="@subheading NOTES:"):
                description=description+" "+contents[index].strip()
                index=index+1
            list.append(description)

            
            # Notes
            notes=""
            index=index+1
            while(contents[index].strip()!="@c"):
                notes=notes+" "+contents[index].strip()
                index=index+1
            list.append(notes)


    #----------- at the end of read parameters have the following format--------------------------------------------------------------------------------------
    # section name1,parameter11,parmeter12....parameter1n,end of subsection,section name2,parameter21,parmeter22....parameter2n,end of subsection...and so on.                    
    #----------- conf.t read complete, processing starts -----------------------------------------------------------------------------------------------------       

    parameters=[]
    index=0
    section=0
    #print parameters[0]
    parameters.append([])

    for index in xrange(len(list)):
        if list[index]=='end of subsection':
            parameters.append([])
            section=section+1
            continue
        x=list[index]
        parameters[section].append(x)

    #print parameters
    return parameters

#return_parameters()

    #---------------------- end of processing ------------------------------
    #          The format of the parameters after processing is as follows
    #   {name of section-1, {parameter-1,data type-1,range-1,default value-1,description-1,notes-1},.......,{parameter-n,data type-n,range-n,default value-n,description-n,notes-n}}
    #   .
    #   .
    #   .
    #   {name of section-m, {parameter-1,data type-1,range-1,default value-1,description-1,notes-1},.......,{parameter-n,data type-n,range-n,default value-n,description-n,notes-n}}
    
