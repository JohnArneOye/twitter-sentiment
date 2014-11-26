'''
Created on 19. nov. 2014

@author: JohnArne
'''

import easygui as eg
import sys
        
def show_windows():
    while 1:
#            title = "Message from test1.py"
#            eg.msgbox("Hello, world!", title)
    
        msg ="Run with which classification model?"
        title = "Classification model"
        models = ["Multinomial Naive Bayes", "Support Vector Machines", "Maximum Entropy"]
        model_choice = str(eg.choicebox(msg, title, models))
    
        msg     = "Use saved preset values?"
        choices = ["Yes","No"]
        choice = eg.buttonbox(msg,choices=choices)
        if str(choice)=="Yes":
            model_preset_functions[model_choice]()
        else:
            model_select_functions[model_choice]()
    
        # note that we convert choice to string, in case
        # the user cancelled the choice, and we got None.
#            eg.msgbox("You chose: " + str(choice), "Survey Result")
        message = "Sentiments over time period something something"
        image = "temporal_sentiments.png"
        eg.msgbox(message, image=image)
        
        msg = "Do you want to continue?"
        title = "Please Confirm"
        if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
            pass  # user chose Continue
        else:
            sys.exit(0)           # user chose Cancel
    
def show_naivebayes_presets():
    """
    Shows a selection of preset running values for Naive Bayes and returns the user selection.
    """
    msg ="Select preset values for Naive Bayes"
    title = "Naive Bayes presets"
    choices = ["Multinomial Naive Bayes", "Support Vector Machines", "Maximum Entropy"]
    preset_choice = eg.choicebox(msg, title, choices)
    pass

def show_svm_presets():
    """
    Shows a selection of preset running values for Suport Vector Machine and returns the user selection.
    """
    msg ="Select preset values for Support Vector Machines"
    title = "SVM presets"
    choices = ["something", "somethingsomething", "something else"]
    preset_choice = eg.choicebox(msg, title, choices)
    pass

def show_me_presets():
    """
    Shows a selection of preset running values for Maximum Entropy and returns the user selection.
    """
    msg ="Select preset values for Maximum Entropy"
    title = "MaxEnt presets"
    choices = ["something", "something else", "aaand more"]
    preset_choice = eg.choicebox(msg, title, choices)
    pass

def show_naivebayes_selection():
    """
    Shows a value input window for Naive Bayes and returns the user selection.
    """
    msg         = "Enter running values for Naive Bayes"
    title       = "Naive Bayes run"
    fieldNames  = ["x","dss","c","range","s","p","cross","stu","thn","pH"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = eg.multenterbox(msg,title, fieldNames)
    
    # make sure that none of the fields was left blank
    while 1:  # do forever, until we find acceptable values and break out
        if fieldValues == None: 
            break
        errmsg = ""
        
        # look for errors in the returned values
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
            
        if errmsg == "": 
            break # no problems found
        else:
            # show the box again, with the errmsg as the message    
            fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
        
    print ("Reply was:", fieldValues)
    pass

def show_svm_selection():
    """
    Shows a value input window for Suport Vector Machine and returns the user selection.
    """
    pass

def show_me_selection():
    """
    Shows a value input window for Maximum Entropy and returns the user selection.
    """
    pass


model_preset_functions = {"Multinomial Naive Bayes": show_naivebayes_presets,
                          "Support Vector Machines": show_svm_presets,
                          "Maximum Entropy": show_me_presets}

model_select_functions = {"Multinomial Naive Bayes": show_naivebayes_selection,
                          "Support Vector Machines": show_svm_selection,
                          "Maximum Entropy": show_me_selection}
