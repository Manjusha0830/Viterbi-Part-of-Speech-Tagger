# Viterbi-Part-of-Speech-Tagger

Python program Viterbi.py that implements the Viterbi algorithm for part-of-speech tagging, as discussed in class. Specifically, your program will have to assign words with their Penn Treebank tag. You will train and test your program on subsets of the Treebank dataset, consisting of documents drawn from various sources, which have been manually annotated with part-of-speech tags.

Programming guidelines:
program should perform the following steps:
❖	Starting with the training file, collect and store all the raw counts required by the Viterbi algorithm. Please make sure to also cover the "beginning of a sentence" in your raw  counts.
❖	Implement the Viterbi algorithm and apply it on the test data. Make sure to strip off the part-of-speech tags in the test data before you make your tag predictions.
❖	Compare the tags predicted by your implementation of the Viterbi algorithm against the provided (gold-standard) tags and calculate the accuracy of your system.
❖	The Viterbi.py program should be run using a command like this: % python Viterbi.py
POS.train POS.test
❖	The program should produce at the standard output the accuracy of the system, as a percentage. It should also generate a file called POS.test.out, which includes the words in the test file along with the part-of-speech tags predicted by the system
