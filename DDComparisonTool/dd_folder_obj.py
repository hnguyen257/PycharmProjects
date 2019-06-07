from os import listdir
import xml.etree.ElementTree as ET

"""
Description:
"""
previous_files = dict()

"""
Description:
"""
class DD_Folder():

    """
    Description:
    """
    information = dict([("manufacturer_id_label", ""), ("manufacturer_id_number", 0),\
                        ("device_type_label", ""), ("device_type_number", 0),\
                        ("rev_label", ""), ("rev_number", 0),\
                        ("dd_rev_label", ""), ("dd_rev_number", 0),\
                        ("device_name", "")])

    """
    Description:
        - (<FILE_NAME> or <FILE_EXTENTION>, <Compute Diff>, <Index in self.files>)
    
    List:
        00 - ddinstal.ini
        01 - .alert
        02 - .fhx
        03 - .mrg
        04 - .ini
        -----------------------
        05 - .alm
        -----------------------
        06 - .map
        07 - .sym
        08 - mmi.dct
        -----------------------
        09 - .fm[s,6,8]
        10 - .dll
    """
    expected_files = [("ddinstal.ini", True), (".alert", True), (".fhx", True), (".mrg", True),\
                      (".ini", True), (".alm", True), (".map", False), (".sym", False),\
                      ("mmi.dct", False), ((".fms", ".fm6", ".fm8"), False), (".dll", False)]


    """
    Description:

    (Key,file_index,value)
    """
    internal_diffs = []



    """
    Description: Initialization of path dependent attributes.
    """
    def __init__(self, path):
        print("\n\n***STARTING:  ---------- DD_Folder.__init__(path) ----------")
        print("  * path: " + str(path))
        self.folder_path = path
        self.files = listdir(path) # return a list of all files inside that folder
        self.file_info = [[-1]]*len(self.files)

        print("  * folder_path: "+str(self.folder_path))
        print("  * files: "+str(self.files))
        print("  * file_info: "+str(self.file_info))
        self.scrape_path()
        self.order_files()
        self.scrape_files()



    """
    Description: Initialization of path dependent attributes.
    """
    def __str__(self):
        ret_str = ""
        ret_str += "* Folder Path: "+str(self.folder_path)+"\n"
        ret_str += "* Files:\n"
        for i in range(len(self.files)):
            ret_str += "  * "+str(i)+". "+str(self.files[i])+"\n"
        ret_str += "*** File Info:\n"
        for i in range(len(self.file_info)):
            ret_str += "  * "+str(i)+". "+str(self.file_info[i])+"\n"
        ret_str += "*** Information:\n"
        for i in self.information:
            ret_str += "  * "+str(i)+": "+str(self.information[i])+"\n"
        ret_str += "*** Expected Files:\n"
        #Took the last index outside the for loop to remove the "\n"
        for i in range(len(self.expected_files) - 1):
            ret_str += "  * "+str(i)+". "+str(self.expected_files[i])+"\n"
        ret_str += "  * "+str(len(self.expected_files) - 1)+". "+str(self.expected_files[len(self.expected_files) - 1])
        return ret_str



    """
    Description: 
    """
    def get_expected_file_index(self, extension):
        if extension[0] != '.':
            extension = '.'+extension
        ef_list = [x[0] for x in self.expected_files]
        if extension not in ef_list:
            return -1
        return ef_list.index(extension)



    """
    Description: 
    """
    def get_file_index(self, i):
        if type(i) == str:
            i = self.get_expected_file_index(i)
        f_list = [x[0] for x in self.file_info]
        if i not in f_list:
            return -1
        return f_list.index(i)



    """
    Description:  Populates the first few values of 'information'
        from the titles of the files in the folders.
    """
    def scrape_path(self):
        print("  ***STARTING:  ---------- DD_Folder.scrape_path() ----------")

        #Find .alert and .sym file
        alert_found, sym_found, dll_found, dll_try_again = False, False, False, False
        alert_values, sym_value, dll_value = ["","",""], "", ""
        for n in self.files:
            if n.endswith(".alert"):
                #parse file name to find dd information
                alert_values = n.split(".")[0].split("_")
                alert_found = True

            if n.endswith(".sym"):
                #parse file name to find dd information
                sym_value = n.split(".")[0][2::]
                sym_found = True

            if n.endswith(".dll"):
                dll_value = ""
                if "_" in n:
                    dll_value = n.split("_")[0]
                    dll_try_again = False
                #The rev_label will have to have been filled prior to this
                elif len(self.information["rev_label"]) > 0:
                    dll_value = n.split(self.information["rev_label"][1])[0]
                    dll_try_again = False
                #If it is not we try again after it is filled below
                else:
                    dll_try_again = True
                dll_found = True

            if sym_found and alert_found and dll_found:
                break
                
        #Populate the corresponding information


        self.information["manufacturer_id_label"] = alert_values[0]
        if (len(alert_values) > 1):
            self.information["device_type_label"] = alert_values[1]
        if (len(alert_values) > 2):
            self.information["rev_label"] = alert_values[2]

        self.information["dd_rev_label"] = sym_value

        if dll_try_again:
            for n in self.files:
                if n.endswith(".dll"):
                    dll_value = n.split(self.information["rev_label"][1])[0]

        self.information["device_name"] = dll_value
        if(len(self.information["manufacturer_id_label"]) > 0):
            self.information["manufacturer_id_number"] = int(self.information["manufacturer_id_label"], 16)
        if (len(self.information["device_type_label"]) > 0):
            self.information["device_type_number"] = int(self.information["device_type_label"], 16)
        if (len(self.information["rev_label"]) > 0):
            self.information["rev_number"] = int(self.information["rev_label"], 16)
        if (len(self.information["dd_rev_label"]) > 0):
            self.information["dd_rev_number"] = int(self.information["dd_rev_label"], 16)


    """
    Description:
    """
    def order_files(self):
        print("  ***STARTING:  ---------- DD_Folder.order_files() ----------")

        len_files = len(self.files) # getting number of files in the DD folder
        files_index = 0 # ?

        file_names = [None] * 11
        # file_names[0] : ddinstal.ini
        file_names[0] = ("ddinstal.ini")
        # file_names[1] : .alert
        file_names[1] = self.information["manufacturer_id_label"]+"_"+self.information["device_type_label"]+"_"+self.information["rev_label"]+".alert"
        # file_names[2] : .fhx
        file_names[2] = self.information["manufacturer_id_label"]+"_"+self.information["device_type_label"]+"_"+self.information["rev_label"]+".fhx"
        # file_names[3] : .mrg
        file_name_0 = self.information["manufacturer_id_label"]+self.information["device_type_label"]+self.information["rev_label"]+self.information["dd_rev_label"]+".mrg"
        rev_label_holder = ""
        dd_rev_label_holder = ""
        if(len(self.information["rev_label"]) > 0):
                rev_label_holder = self.information["rev_label"][1]
        if (len(self.information["dd_rev_label"]) > 0):
                dd_rev_label_holder = self.information["dd_rev_label"][1]
        file_name_1 = self.information["device_name"]+rev_label_holder+dd_rev_label_holder+".mrg"
        file_names[3] = (file_name_0, file_name_1)
        # file_names[4] : .ini
        file_names[4] = self.information["rev_label"]+self.information["dd_rev_label"]+".ini"
        #--------------------------------------
        # file_names[5] : .alm
        file_names[5] = self.information["manufacturer_id_label"]+"_"+self.information["device_type_label"]+"_"+self.information["rev_label"]+".alm"
        # file_names[6] : .map
        file_names[6] = self.information["rev_label"]+self.information["dd_rev_label"]+".map"
        # file_names[7] : .sym
        file_names[7] = self.information["rev_label"]+self.information["dd_rev_label"]+".sym"
        # file_names[8] : mmi.dct
        file_names[8] = "mmi.dct"
        #--------------------------------------
        # file_names[9] : .fm[s,6,8]
        file_name_0 = self.information["rev_label"]+self.information["dd_rev_label"]+".fms"
        file_name_1 = self.information["rev_label"]+self.information["dd_rev_label"]+".fm6"
        file_name_2 = self.information["rev_label"]+self.information["dd_rev_label"]+".fm8"
        file_names[9] = (file_name_0, file_name_1, file_name_2)
        # file_names[10] : .dll
        file_name_0 = self.information["device_name"]+"_"+self.information["rev_label"]+self.information["dd_rev_label"]+".dll"
        file_name_1 = self.information["device_name"]+rev_label_holder+dd_rev_label_holder+".dll"
        file_names[10] = (file_name_0, file_name_1)


        # file_name is list of possible DD files (right now there are 11 known file types)

        # going through the list of possible file types
        for fni in range(len(file_names)):
            #if not a list
            if type(file_names[fni]) == str:
                # going through the DD folder
                for i in range(len_files):
                    print self.files[i]
                    print "  " + file_names[fni]
                    # if the file names in the DD folder match the file type at the current index, then:
                    if self.files[i] == file_names[fni]:
                        if i != 0: #why?
                            self.files[files_index], self.files[i] = self.files[i], self.files[files_index]
                            self.file_info[files_index] = [fni]
                            files_index += 1
                        break
            #if is a list
            elif type(file_names[fni]) == tuple:
                for i in range(len_files):
                    if self.files[i] in file_names[fni]:
                        if i != 0:
                            self.files[files_index], self.files[i] = self.files[i], self.files[files_index]
                            self.file_info[files_index] = [fni]
                            files_index += 1
                        break
            if files_index == len_files:
                break



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_files(self):
        print("  ***STARTING:  ---------- DD_Folder.scrape_files() ----------")
        self.scrape_ddinstal()
        self.scrape_alert()
        self.scrape_fhx()
        self.scrape_mrg()
        self.scrape_ini()
        self.scrape_alm()
        print("  ***ENDING:  ---------- DD_Folder.scrape_files() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_ddinstal(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_ddinstal() ----------")
        print("    ***ENDING:  ---------- DD_Folder.scrape_ddinstal() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_alert(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_alert() ----------")
        alert_index = self.get_expected_file_index("alert")
        if alert_index == -1:
            print("#### - ALERT FILE NOT FOUND IN OBJECT - FIX CODE")
            return alert_index
        alert_file_index = self.get_file_index(alert_index)
        if alert_file_index == -1:
            print("      * No \'Alert File\' found")
            return alert_file_index
        self.file_info[alert_file_index].append(ET.parse(self.folder_path+"/"+self.files[alert_file_index]).getroot())
        # Folder Value Checking
        print("    ***ENDING:  ---------- DD_Folder.scrape_alert() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_fhx(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_fhx() ----------")
        print("    ***ENDING:  ---------- DD_Folder.scrape_fhx() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_mrg(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_mrg() ----------")
        print("    ***ENDING:  ---------- DD_Folder.scrape_mrg() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_ini(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_ini() ----------")
        print("    ***ENDING:  ---------- DD_Folder.scrape_ini() ----------")



    """
    Description:

        - internal_diffs = [(Key, file_index, line_number, value),...]
    """
    def scrape_alm(self):
        print("    ***STARTING:  ---------- DD_Folder.scrape_alm() ----------")
        print("    ***ENDING:  ---------- DD_Folder.scrape_alm() ----------")



    """
    Description:
    """
    def temp(self):
        pass






"""
Discription: 
"""
def get_dd_file(path, file_type=-1):
    # Check "previous_files" Cache
    global previous_files
    if path in previous_files:
        return previous_files[path]

    #If file_type is > -1 and < 5 and route properly
    dd_file = ""
    if file_type > -1:
        if file_type == 0:
            dd_file = get_ddini_file(path)
        elif file_type == 1:
            dd_file = get_alert_file(path)
        elif file_type == 2:
            dd_file = get_fhx_file(path)
        elif file_type == 3:
            dd_file = get_mrg_file(path)
        elif file_type == 4:
            dd_file = get_ini_file(path)
        elif file_type == 5:
            dd_file = get_alm_file(path)
        else:
            print("###ERROR - illegal index used in - get_dd_file() - Expected index [(-1) - 4], Recieved: file_type")
            dd_file =  -1

    #Else: control flow through extension
    else:
        file_type = path.split(".")
        file_type = file_type[len(file_type) - 1]
        if file_type == "ini":
            dd_file = get_ini_file(path)
        elif file_type == "alert":
            dd_file = get_alert_file(path)
        elif file_type == "fhx":
            dd_file = get_fhx_file(path)
        elif file_type == "mrg":
            dd_file = get_mrg_file(path)
        elif file_type == "alm":
            dd_file = get_alm_file(path)
        else:
            with open(path) as f:
                dd_file = f.read().splitlines()
            dd_file = [dd_file[i] for i in range(len(dd_file))]

    previous_files.update({path: dd_file})
    return dd_file



"""
Discription: 
"""
def get_ddini_file(path):
    with open(path) as f:
        ddini_file = f.read().replace('\x00', '').replace('\xff', '').replace('\xfe', '').splitlines()
    ddini_file = [ddini_file[i] for i in range(len(ddini_file))]
    return ddini_file



"""
Discription: 
"""
def get_alert_file(path):
    with open(path) as f:
        alert_file = f.read().splitlines()
    alert_file = [alert_file[i] for i in range(len(alert_file))]
    return alert_file



"""
Discription: 
"""
def get_fhx_file(path):
    with open(path) as f:
        fhx_file = f.read().replace('\x00', '').replace('\xff', '').replace('\xfe', '').splitlines()
    fhx_file = [fhx_file[i] for i in range(len(fhx_file))]
    return fhx_file



"""
Discription: 
"""
def get_mrg_file(path):
    with open(path) as f:
        mrg_file = f.read().replace('\x00', '').replace('\xff', '').replace('\xfe', '').splitlines()
    mrg_file = [mrg_file[i] for i in range(0, len(mrg_file), 2)]
    return mrg_file



"""
Discription: 
"""
def get_ini_file(path):
    with open(path) as f:
        ini_file = f.read().splitlines()
    ini_file = [ini_file[i] for i in range(len(ini_file))]
    return ini_file



"""
Discription: 
"""
def get_alm_file(path):
    with open(path) as f:
        alm_file = f.read().replace('\x00', '').replace('\xff', '').replace('\xfe', '').splitlines()
    alm_file = [alm_file[i] for i in range(0, len(alm_file), 2)]
    return alm_file



"""
Discription: 
    (Existance - Based, Name or None, Name or None)
    (Non Existance - Based, Field, Value 0, Value 1)
 - [(True, "File", File Name 0, File Name 1), (False, Field, value 0, value 1), ... (True, "File", File Name 0, File Name 1), (False, Field, value 0, value 1), ...]
"""
def fbf_diffs(obj_0, obj_1):
    ret_diffs = []


    file_diffs = []

    #Iterate through all files
    index0 = obj_0.get_file_index("alert")
    index1 = obj_1.get_file_index("alert")
    if index0 != -1 and index1 != -1:
        et0 = obj_0.file_info[index0][1]
        et1 = obj_1.file_info[index1][1]
        #file_diffs.extend([True, ".alert", obj_0.files[index0], obj_1.files[index1]])
        file_diffs.append([True, ".alert", obj_0.files[index0], obj_1.files[index1], alert_fbfd(et0, et1)])
    elif index0 != -1:
        file_diffs.append((False, ".alert", obj_0.files[index0], None))
    elif index1 != -1:
        file_diffs.append((False, ".alert", None, obj_1.files[index1]))

    #for i in file_diffs:
    #    print(i)
    #print(file_diffs)
    print_obj(file_diffs, "")
    ret_diffs.extend(file_diffs)

    return ret_diffs

def print_obj(obj, spacing):
    for i in obj:
        if type(i) == list:
            if type(i[3]) == list or type(i[3]) == tuple:
                print(spacing+str(i[:3]))
                print_obj(i[3], spacing+"  ")
            else:
                print(spacing+str(i[:4]))
                print_obj(i[4], spacing+"  ")

        elif type(i) == tuple:
            if len(i) == 4 and (len(str(i[2])) > 15 or len(str(i[3])) > 15):
                print(spacing+"("+str(i[0])+", "+str(i[1])+", "+str(i[2])[:15]+", "+str(i[3])[:15]+")")
            else:
                print(spacing+str(i))
        elif len(str(i))>10:
            print(spacing+str(i)[:10])
        else:
            print(spacing+str(i))

"""
Discription: 

 - [(True, "Variable", Var Name 0, Var Name 1), (False, Field, value 0, value 1), ... (True, "Alert", Alert id 0, Alert id 1), (False, Field, value 0, value 1), ...]
"""
def alert_fbfd(et0, et1):
    alternate_var_names = [("device_specific_status", "xmtr_specific_status")]
    ret_diffs = []

    root_field_list0 = [i.tag for i in et0]
    root_field_list1 = [i.tag for i in et1]
    root_non_visited1 = range(len(et1))

    for root_i0 in range(len(et0)):

        root_field_tag = root_field_list0[root_i0]
        if root_field_tag in root_field_list1:

            # remove index1 from root_non_visited1
            root_field0 = et0[root_i0]
            root_field1 = et1.find(root_field_tag)
            root_non_visited1.remove(root_field_list1.index(root_field_tag))
            # ------------------------------------------------------------------------------------------------------------------------------------------
            # ----BEGIN VARIABLE LOOP-------------------------------------------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------------------------------------------------------------------
            if root_field_tag == "VariableList":

                var_list0 = root_field0
                var_list1 = root_field1
                var_name_list0 = [i.find("Name").text for i in var_list0]
                var_name_list1 = [i.find("Name").text for i in var_list1]
                var_non_visited1 = range(len(var_list1))

                for var_list_i0 in range(len(var_list0)):

                    var_name0 = var_name_list0[var_list_i0]
                    var_name1 = None

                    if var_name0 in var_name_list1:
                        var_name1 = var_name0
                    else:
                        for alt_var in alternate_var_names:
                            var_name_temp = ""
                            if alt_var[0] in var_name0:
                                var_name_temp = var_name0.replace(alt_var[0], alt_var[1])
                            elif alt_var[1] in var_name0:
                                var_name_temp = var_name0.replace(alt_var[1], alt_var[0])
                            if var_name_temp in var_name_list1:
                                var_name1 = var_name_temp
                                break

                    if var_name1 != None:
                        var_diffs = [True, "variable", var_name0, var_name1, []]
                        # remove index1 from var_non_visited1
                        var0 = var_list0[var_list_i0]
                        var1 = var_list1[var_name_list1.index(var_name1)]
                        var_non_visited1.remove(var_name_list1.index(var_name1))

                        #Compare Fields
                        var_field_list0 = [i.tag for i in var0]
                        var_field_list1 = [i.tag for i in var1]
                        var_field_non_visited1 = range(len(var1))
                        for var_i0 in range(len(var0)):

                            var_field_tag = var_field_list0[var_i0]
                            if var_field_tag in var_field_list1:
                                
                                var_field0 = var0[var_i0]
                                var_field1 = var1.find(var_field_tag)
                                var_field_non_visited1.remove(var_field_list1.index(var_field_tag))

                                if var_field_tag == "AlertList":

                                    alert_list0 = var_field0
                                    alert_list1 = var_field1
                                    alert_value_list0 = [i.find("Value").text for i in alert_list0]
                                    alert_value_list1 = [i.find("Value").text for i in alert_list1]
                                    alert_non_visited1 = range(len(alert_list1))

                                    for alert_list_i0 in range(len(alert_list0)):

                                        alert_value = alert_value_list0[alert_list_i0]
                                        if alert_value in alert_value_list1:
                                            alert_diffs = [True, "alert", alert_value, []]
                                            # remove index1 from var_non_visited1
                                            alert0 = alert_list0[alert_list_i0]
                                            alert1 = alert_list1[alert_value_list1.index(alert_value)]
                                            alert_non_visited1.remove(alert_value_list1.index(alert_value))

                                            #Compare Fields
                                            alert_field_list0 = [i.tag for i in alert0]
                                            alert_field_list1 = [i.tag for i in alert1]
                                            alert_field_non_visited1 = range(len(alert1))
                                            for alert_i0 in range(len(alert0)):

                                                alert_field_tag = alert_field_list0[alert_i0]
                                                if alert_field_tag in alert_field_list1:
                                                    
                                                    alert_field0 = alert0[alert_i0]
                                                    alert_field1 = alert1.find(alert_field_tag)
                                                    alert_field_non_visited1.remove(alert_field_list1.index(alert_field_tag))

                                                    if alert_field0.text != alert_field1.text:
                                                        # Append Difference
                                                        alert_diffs[3].append((False, alert_field_tag, alert_field0.text.replace("\n", ""), alert_field1.text.replace("\n", "")))
                                                else:
                                                    # Append missing
                                                    alert_diffs[3].append((False, "missing alert_field", alert_field_tag, None))
                                            # Append var1 missing fields
                                            if len(alert_field_non_visited1) > 1:
                                                alert_diffs[3].extend([(False, "missing alert_field", None, alert_field_list1[i]) for i in alert_field_non_visited1])
                                            # Append alert_diffs
                                            if len(alert_diffs) > 3:
                                                var_diffs[4].append(alert_diffs)
                                        else:
                                            # Add Missing
                                            var_diffs[4].append((False, "missing alert", alert_value, None))

                                    if len(alert_non_visited1) > 0:
                                        var_diffs[4].extend([(False, "missing alert", None, alert_value_list1[i]) for i in alert_non_visited1])

                                elif var_field0.text != var_field1.text:
                                    # Append Difference
                                    var_diffs[4].append((False, var_field_tag, var_field0.text.replace("\n", ""), var_field1.text.replace("\n", "")))
                            else:
                                # Append missing
                                var_diffs[4].append((False, "missing var_field", var_field_tag, None))
                        # Append var1 missing fields
                        if len(var_field_non_visited1) > 1:
                            var_diffs[4].extend([(False, "missing var_field", None, var_field_list1[i]) for i in var_field_non_visited1])
                        # Append var_diffs
                        if len(var_diffs) > 4:
                            ret_diffs.append(var_diffs)
                    else:
                        # Add Missing
                        ret_diffs.append((False, "missing variable", var_name0, None))

                if len(var_non_visited1) > 0:
                    ret_diffs.extend([(False, "missing variable", None, var_name_list1[i]) for i in var_non_visited1])
            # ------------------------------------------------------------------------------------------------------------------------------------------
            # ----END VARIABLE LOOP---------------------------------------------------------------------------------------------------------------------
            # ------------------------------------------------------------------------------------------------------------------------------------------
            elif root_field0.text != root_field1.text:
                ret_diffs.append((False, root_field_tag, root_field0.text, root_field1.text))

        else:
            # Append Missing for this
            ret_diffs.append((False, "missing field", root_field_tag, None))

    # Appending Missings for the remainder of indexes in root_non_visited1
    if len(root_non_visited1) > 0:
        ret_diffs.extend([(False, "missing field", None, et1[i].tag) for i in root_non_visited1])

    return ret_diffs









