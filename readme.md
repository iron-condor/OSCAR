What is OSCAR?

Open Source Computer Assistant Robot, or OSCAR, is a desktop assistant inspired by predecessors such as Cortana, Siri, and Google Assistant. Unlike these other assistants, OSCAR was built with two concepts in mind - privacy, and customizability.

Configuration

OSCAR generates a few files when you first start him. He'll notify you as to where they're at, but for reference, they're located at ~/.config/oscar/inputs and ~/.config/oscar/responses
Both are formatted using JSON, and they each have their own purpose. The inputs file controls what strings and keywords OSCAR interprets to be a certain command. The responses file manages OSCAR's responses to various stimuli. With these two files, you can customize OSCAR to be able to use and understand different vernacular. If you plan on adding new functions to OSCAR, you'll need to update these files accordingly.

Dependencies

duckduckgo-python3
xdg-utils
