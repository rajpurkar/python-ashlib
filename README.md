# AshLib
A Python library containing a multitude of varied functionality. This library is still very much a rough work in progress.

### Installation

To install this library, first clone this repository. Then navigate to the python-ashlib directory from the terminal and run the setup.py script with the argument "install" (i.e. "python setup.py install"). You may have to run that command with root permissions (i.e. "sudo python setup.py install").

To use the ling package's cnlp.py and sentiment.py modules' functionality, one must download the most recent version of the Stanford CoreNLP build from http://nlp.stanford.edu/software/corenlp.shtml and supply both a relative or absolute file path to the directory in which it resides and its version to the CoreNLP constructor.

To use the ling package's named entity recognition functionalitywork, one must download the most recent version of the Stanford Named Entity Recognizer from http://nlp.stanford.edu/software/CRF-NER.shtml#Download and supply both a relative or absolute file path to the directory in which it resides and its version to the NERTagger constructor.

Why don't we just include these external Stanford libraries in AshLib? Both are extremly large (on the order of 150 MB each) and we didn't want to make AshLib that heavy. Furthermore, if you already have coppies of the Stanford libraries on your machine, as we suspect many programmers already working on NLP-related projects are, you don't have to download the huge Stanford libraries a second time; you can point AshLib to their existing locations.
