![OSCAR](https://i.imgur.com/zMjKKeP.png)


### **What is OSCAR?**
---

**O**pen **S**ource **C**omputer **A**ssistant **R**obot, or **OSCAR**, is a desktop assistant inspired by predecessors such as Cortana, Siri, and Google Assistant. Unlike these other assistants, OSCAR was built with two concepts in mind - privacy, and customizability.


### **Configuration**
---

OSCAR generates a few files when you first start him. He'll notify you as to where they're at, but for reference, they're located at `~/.config/oscar/inputs` and `~/.config/oscar/responses`
Both are formatted using JSON, and they each have their own purpose.


The inputs file controls what strings and keywords OSCAR interprets to be a certain command.


The responses file manages OSCAR's responses to various stimuli.


With these two files, you can customize OSCAR to be able to use and understand any type of vernacular. If you plan on adding new functions to OSCAR, you'll need to update these files accordingly.

### **Features**
---
OSCAR is still in its youth, so expect more features in the near future.

At the moment, OSCAR can
* Tell you the time
* Look up and summarize things for you
* Schedule a shutdown
* Schedule generic commands
* Help you make decisions (*Should I stay in for the night, or go out and eat?*)
* Tell you jokes (using [https://github.com/pyjokes/pyjokes](pyjokes!))
* Launch programs for you

### **Dependencies**
---

duckduckgo-python3

xdg-utils (if using linux)

tkinter

jsonpickle

### **Getting started**

Starting with OSCAR is easy - just open the program in a terminal and start talking to him.
