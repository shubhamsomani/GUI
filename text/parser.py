# A text parser which operates on conf.t
# Author : Shubham Somani

def return_parameters():
    
    #-----------section on parsing from the conf.t file---------------------

    data=open("conf.t")
    contents=data.readlines()
    list=[]
    flag=0
    start=0
    for index in range(0,len(contents)):
        if "@section" in contents[index]:               
            s=contents[index].split("@section")
            if s[1].strip()=="Classic API Configuration":
                start=1
        if "@section" in contents[index] and start==1:               
            s=contents[index].split("@section")
            #print s[1].strip()
            if flag==1:
                list.append("end of subsection")
            list.append(s[1].strip())
            flag=1
        if "@findex" in contents[index] and flag==1:
            s=contents[index].split("@findex")
            #print s[1].strip()
            list.append(s[1].strip())
            while(contents[index].strip()!="@end table"):
                index=index+1
                if(contents[index].strip()=="@item DATA TYPE:"):
                    #print contents[index+1]
                    list.append(contents[index+1])
                if(contents[index].strip()=="@item DEFAULT VALUE:"):
                    index=index+1
                    input_string=""
                    while(contents[index].strip()!="@end table"):
                        input_string=input_string+contents[index].strip()
                        index=index+1
                    if("@code{" in input_string):
                        string=input_string.split("@code{")
                        temp=string[0]+string[1]
                        temp2=temp.split("}")
                        string_after_operations=temp2[0]+" "+temp2[1]
                        list.append(string_after_operations)
                    else:
                        list.append(input_string)
            
    #----------- conf.t read complete, processing starts --------------------
            
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

return_parameters()

    #---------------------- end of processing ------------------------------
    #          The format of the parameters after processing is as follows
    #   {name of section-1, {parameter-1,data type-1,default value-1},.......,{parameter-n,data type-n,default value-n}}
    #   .
    #   .
    #   .
    #   {name of section-m, {parameter-1,data type-1,default value-1},.......,{parameter-n,data type-n,default value-n}}
    
