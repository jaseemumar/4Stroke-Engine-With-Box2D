#!/usr/bin/python3
import os, sys, re

def parsed(line):
    if "\\subsection*" in line: return "<h2>"+re.search('\{(.*)\}',line).group(1)+"</h2>"
    elif "\\section*" in line:return "<h1>"+re.search('\{(.*)\}',line).group(1)+"</h1>"
    elif "\\textbf" in line:return "<b>"+re.search('\{(.*)\}',line).group(1)+"<br/></b>"
    elif "\\item" in line:return re.search('(\\item)(.*)',line).group(2) + "<br/>"
    
    #~ elif "\\par" in line: return "<p>"+re.search('\\par (.*)',line).group(1)+"</p>"
    #~ elif "\\includegraphics" in line: return "<img src=%s width=%d height=%d>"%(re.search(r'\{([\w.\d]+)\}',line).group(), re.search)
    elif "\\includegraphics" in line:
        if "machine" in line: return "<img class = 'img' src = '../data/machine.png' width = 350px height = 200px align = 'middle' >"
        elif "lawnMower" in line: return "<img class = 'img' src = '../data/lawnMower.png' width = 350px height = 300px align = 'middle' >"
        elif "pistonAssembly" in line: return "<img class = 'img' src = '../data/pistonAssembly.png' width = 350px height = 300px align = 'middle' >"
        elif "crankShaft" in line: return "<img class = 'img'  src = '../data/crankShaft.png' width = 350px height = 300px align = 'middle' >"
        elif "bladeGear" in line: return "<img class = 'img' src = '../data/bladeGear.png' width = 350px height = 300px align = 'middle' >"
        elif "release_mode" in line: return "<img class = 'img' src = '../data/release_mode.png' width = 850px height = 100px align = 'middle' >"
        elif "debug_mode" in line: return "<img class = 'img' src = '../data/debug_mode.png' width = 850px height = 300px align = 'middle' >"
        else: return ""
    elif "\\\\" in line: return "<br/>"
    #~ elif "" in line: return "<br/>"
    elif '\\' in line: return ""
    elif True:
        return re.search('(.*)',line).group(1)
    else : return ""
def main():
    texfile=open("data/g20_project_report.tex")
    ofile=open("doc/g20_project_htmlreport.html",'w')
    start = False
    end = False
    ofile.write("<html><head><title>Interpretation of Lab 5</title><link rel='stylesheet' href='index.css' type='text/css'/></head><body><div id='container'>")
    
    for line in texfile:
        #~ print(line)
        if "\\begin{document}" in line:
            start = True
        elif start and "\\end{document}" in line:
            end = True
        if start and not end: ofile.write(parsed(line))
        if end: break
    ofile.write("</div></body></html>")
            
            
        
main()
