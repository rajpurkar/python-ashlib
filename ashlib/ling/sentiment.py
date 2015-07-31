import os
import sys
import re
import subprocess

import ashlib.util.file
import ashlib.util.stats
import ashlib.util.list

SENTIMENT_MAP = {"Very negative": 1, "Negative": 2, "Neutral": 3, "Positive": 4, "Very positive": 5}

## TODO: keep the allowance of arg being string or list? First and last chunks of code both depend on it

def calc(arg):
    if isinstance(arg, list): statements = arg
    elif isinstance(arg, set): statements = list(arg)
    elif isinstance(arg, basestring): statements = [arg]
    else: raise ValueError("Input must be single string, list of strings or set of strings.")
    
    # Format input:
    statements = ashlib.util.list.replace(statements, lambda statement: " ".join(statement.strip().split()))
    ashlib.util.file.overwrite(os.path.join(os.path.dirname(__file__), "stanford-corenlp-full-2015-04-20", "input.txt"), "\n".join(statements))
    
    # Call CoreNLP:
    command = "java -cp \"*\" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -file input.txt"
    coreNlpDir = os.path.join(os.path.dirname(__file__), "stanford-corenlp")
    rawOutput = subprocess.check_output(command, cwd=coreNlpDir, stderr=subprocess.STDOUT, shell=True)
    
    # Format output:
    outputStartKey = "Adding annotator sentiment"
    output = rawOutput[rawOutput.find(outputStartKey) + len(outputStartKey):].strip()
    outputParts = ashlib.util.list.replace(output.split("\n"), lambda item: item.strip())
    outputTuples = []
    for index in range(len(outputParts) / 2):
        outputTuples.append((outputParts[2 * index], outputParts[2 * index + 1]))
    
    # Calculate final scores:
    scores = []
    currScores = []
    currStatementIndex = 0
    currStatement = statements[currStatementIndex]
    
    for sentence, sentiLabel in outputTuples:
        if sentence not in currStatement:
            scores.append(ashlib.util.stats.mean(currScores))
            currScores = []
            currStatementIndex += 1
            currStatement = statements[currStatementIndex]
        currScores.append(SENTIMENT_MAP[sentiLabel])
        
    if len(currScores) > 0: 
        scores.append(ashlib.util.stats.mean(currScores))
    
    if isinstance(arg, basestring): return scores[0]
    else: return scores
