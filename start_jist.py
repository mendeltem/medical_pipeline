#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 19:36:33 2021

@author: temuuleu
"""

import subprocess
import os
import argparse

import xml.etree.ElementTree as ET
import re
import subprocess as sp
from os import system, name


def combine_paths(paths=[]):
    """
    combin paths together
    
    """
    
    
    combined_pat = ""

    for path in paths:
        combined_pat+= path + "/"

    
    if "//" in combined_pat:
        combined_pat = combined_pat.replace('//', '/')
    
    if "///" in combined_pat:
        combined_pat = combined_pat.replace('///', '//') 

    if "////" in combined_pat:
        combined_pat = combined_pat.replace('////', '//')     
        
        
    while '/' == combined_pat[-1]:
        combined_pat = combined_pat[:-1]
        
        
    return combined_pat

def clear():
    """clear console screen"""""
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
        
def is_file(path_name):
    """check if the given string is a file"""
    if re.search("\.[a-zA-Z]+$", os.path.basename(path_name)):
        return True
    else:
        return False

def is_directory(path_name):
    
    #path_name = "/persDaten/MRT_daten_manual/output."
    """check if the given string is a directory"""
    
    ewp = os.path.basename(path_name).endswith('.')

    if not ewp and not is_file(path_name) and not len(os.path.basename(path_name))  == 0:
        return True
    else:
        return False

def create_dir(output_path):
    """creates a directory of the given path"""
    if not os.path.exists(output_path) and is_directory(output_path):
        os.makedirs(output_path)
        

def modify_layout(new_patient_dir="",
                  mprage ="",
                  mprage_dir="",
                  flair="",
                  flair_dir=""):
    """modify   testlayout.xml 
    
    
    """
    layout_path="layouts/new.LayoutXML"
    
    print("layout_path", layout_path)
    
    tree = ET.parse(layout_path)
    root = tree.getroot()
    
    root[0][2].text = 'file:'+new_patient_dir+"/"
    
    #modules
    for i,elem in enumerate(root[1]):
        
        #print(elem.tag)
        label = elem.find('label')
    
        if "Lesions Statistics" in label.text:
            #print("label ", label.text)
            ls_inputParams = elem.find("inputParams")
            ls_children = ls_inputParams.find("children")
            
            ls_file_path = ls_children[6].find("file")
            ls_file_uri  = ls_children[6].find("uri")
            
            #print("file_label ", ls_file_path.text)
            #print("file_name ", ls_file_uri.text)
            
            #update
            ls_file_path.text =  new_patient_dir
            ls_file_uri.text  = 'file:'+new_patient_dir+"/"
    
    
        if "T1 MPRAGE" in label.text:
            #print("label ", label.text)
            mprage_inputParams = elem.find("inputParams")
            mprage_children = mprage_inputParams.find("children")
            
            #child_label = mprage_children[1].find('label')
            mprage_childer_child = mprage_children[1].find("children")
            mprage_fileParams = mprage_childer_child[0].find("fileParams")
            mprage_file = mprage_fileParams.find("file")
            mprage_file_label = mprage_file.find("label")
            mprage_file_name  = mprage_file.find("name")
            mprage_file_file_path = mprage_file.find("file")
            mprage_file_uri = mprage_file.find("uri")
            
            
            mprage_file_label.text = mprage
            mprage_file_name.text  = mprage
            mprage_file_file_path.text = mprage_dir
            mprage_file_uri.text       = 'file:'+mprage_dir
            
            #print("file_label ", mprage_file_label.text)
            #print("file_name ", mprage_file_name.text)
            #print("file_file ", mprage_file_file_path.text)
            #print("file_uri ", mprage_file_uri.text)
                    
            
        if "FLAIR" in label.text:
            #print("label ", label.text)
            flair_inputParams = elem.find("inputParams")
            flair_children = flair_inputParams.find("children")
            
            #child_label = flair_children[1].find('label')
            flair_childer_child = flair_children[1].find("children")
            flair_fileParams = flair_childer_child[0].find("fileParams")
            flair_file = flair_fileParams.find("file")
            flair_file_label = flair_file.find("label")
            flair_file_name  = flair_file.find("name")
            flair_file_file = flair_file.find("file")
            flair_file_uri = flair_file.find("uri")
            
            #print("file_label ", flair_file_label.text)
            #print("file_name ", flair_file_name.text)
            #print("file_file ", flair_file_file.text)
            #print("file_uri ", flair_file_uri.text)
            
            flair_file_label.text     = flair
            flair_file_name.text      = flair
            flair_file_file.text      = flair_dir
            flair_file_uri.text       = 'file:'+flair_dir
                    

    test_xml_str = ET.tostring(root, encoding='utf-8').decode()
    new_xml = '<?xml version="1.0" encoding="UTF-8"?>'+test_xml_str
    test_layout = new_patient_dir+"personal_layout.LayoutXML"
    text_file = open(test_layout, "w")
    text_file.write(new_xml)
    text_file.close()
    
    return test_layout


clear()

parser = argparse.ArgumentParser(description='Mipav Pipeline')

parser.add_argument('data_path', metavar='D', type=str, nargs='+',
                    help='data path for input')


parser.add_argument('output_path', metavar='O', type=str, nargs='+',
                    help='ouput directory where the images and statistics are created')

args = parser.parse_args()
daten = args.data_path[0]
output_dir = args.output_path[0]


#daten              = "/home/temuuleu/CSB_NeuroRad/temuuleu/Projekts/Belove/Belove_daten"
#output_dir         = "/home/temuuleu/CSB_NeuroRad/temuuleu/Projekts/Belove/new_Belove_output_2"


#collect all patien dir
all_data_dir_list = [combine_paths([daten,directory]) for directory in os.listdir(daten) if not "." in directory]

for patien_idx , patient_path in enumerate(all_data_dir_list):
    #if mprage is found
    found_mprage = 0
    #if flare is found
    found_flare  = 0
    #try mipav
    mipav_end  = 1
    #search for mul in roy
    mul_bool = 0
    #patient id or name
    patien_dir_name = os.path.basename(patient_path)    
    #list every data in patient directory
    patient_data = os.listdir(patient_path)
    
    try_id = 5

    for data in patient_data:
        if "mprage_" in data.lower() and data.endswith('.nii'):
            
            mprage = data
            found_mprage = 1
            
        if "mul" in data:
            if "flair_" in data.lower() and (data.endswith('.nii') or data.endswith('.nii.gz'))\
                and not "roi" in data.lower() and\
                "mul" in data:
                
                flair = data
                found_flare  = 1   
                
                mul_bool =1
 
        if not mul_bool:
    
            if "flair_" in data.lower() and data.endswith('.nii') and not "roi" in data.lower():
                
                flair = data
                found_flare  = 1    
        
    if found_mprage == 1 and found_flare == 1:
        
        patient_out_put_dir = combine_paths([output_dir,patien_dir_name])+"/"
        mprage_dir          = combine_paths([patient_path,mprage])+"/"
        flair_dir           = combine_paths([patient_path,flair])+"/"
        new_patient_dir     = combine_paths([output_dir,patien_dir_name])+"/"
        
        
        output_string = "Patient "+patien_dir_name+"\n"\
                        +"mprage:          " +mprage+"\n"\
                        +"mprage_dir:      " +mprage_dir+"\n"\
                        +"flair:           " +flair+"\n"\
                        +"flair_dir:       " +flair_dir+"\n"\
                        +"new_patient_dir  " +new_patient_dir+"\n"

        print(output_string)

        if not os.path.exists(new_patient_dir):
            os.makedirs(new_patient_dir)
        
        new_patient_layout = modify_layout(new_patient_dir,mprage,
                      mprage_dir,flair,flair_dir)
        
          
        while(mipav_end):
            
            try:
                try_id +=1
                print("")
                print("Running MIPAV Script")
                print("")
                
                layout_command = "sh layout_jist_java.sh "+new_patient_layout +" " +new_patient_dir
                
                if try_id == 1:
                    os.system(layout_command)
                output = sp.getoutput(layout_command)
                print(output)
                #output = subprocess.check_output(layout_command, shell=True)
                
                log_string = str(output_string)+str(output)
                
                #output = sp.getoutput("pwd")
                mipav_text_path = new_patient_dir+"mipav_log_"+str(try_id)+".txt"       
                    
                mipav_output = open(mipav_text_path, "w")
                mipav_output.write(log_string)
                mipav_output.close()
                
                if "FAILED" in mipav_output:
                    
                    mipav_end -= 1
                    print("mipav FAILED: trys : ",mipav_end)
                else:
                    mipav_end = 0
                    
            
            except:
                mipav_end -= 1
                print("mipav failed: trys : ",mipav_end)
        