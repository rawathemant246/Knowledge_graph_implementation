import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt



def getSentence(text):
    nlp = English()
    nlp.add_pipe("sentencizer")
    document = nlp(text)
    return [sent.text.strip() for sent in document.sents]

def printToken(token):
    print(token.text, "->", token.dep_)

def appendChunk(original, chunk):
    return original + ' ' + chunk

def isRelationalCandidate(token):
    deps = ["ROOT", "adj", "attr", "agent", "amod"]
    return any(subs in token.dep_ for subs in deps)


def isContructionCandidate(token):
    deps = ["compound", "prep", "conj", "dobj"]
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens):
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    
    for token in tokens:
        printToken(token)
        
        if "punct" in token.dep_:
            continue
        
        if isRelationalCandidate(token):
            relation = appendChunk(relation, token.lemma_)
        
        if isContructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(subjectConstruction, token.text)
            
            if objectConstruction:
                objectConstruction = appendChunk(objectConstruction, token.text)
        
        if "subj" in token.dep_:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        
        if "obj" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''
    
    print(subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())




def processSentence(sentence):
    
    tokens = nlp_model(sentence)  
    return processSubjectObjectPairs(tokens)

def printGraph(triples):
    G = nx.Graph()
    G.add_edges_from([(t[0], t[1]) for t in triples] + [(t[1], t[2]) for t in triples])
    
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(12, 8))
    
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='lightblue', alpha=0.9,
            labels={node: node for node in G.nodes()},
            )
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    


if __name__ == "__main__":
    
    text = "Black holes are some of the strangest and most fascinating objects in space. " \
       "They're extremely dense, with such strong gravitational attraction that not even light can escape their grasp. " \
       "The Milky Way could contain over 100 million black holes, though detecting these gluttonous beasts is very difficult. " \
       "At the heart of the Milky Way lies a supermassive black hole — Sagittarius A*. " \
       "The colossal structure is about 4 million times the mass of the sun and lies approximately 26,000 light-years away from Earth, according to a statement from NASA."
    
    sentences = getSentence(text)
    
    nlp_model = spacy.load('en_core_web_sm')
    
    triples = []
    print(text)
    
    for sentence in sentences:
        triples.append(processSentence(sentence))
    
    printGraph(triples)



# text = "London is the capital and largest city of England and the United Kingdom. Standing on the River " \
#            "Thames in the south-east of England, at the head of its 50-mile (80 km) estuary leading to " \
#            "the North Sea, London has been a major settlement for two millennia. " \
#            "Londinium was founded by the Romans. The City of London, " \
#            "London's ancient core − an area of just 1.12 square miles (2.9 km2) and colloquially known as " \
#            "the Square Mile − retains boundaries that follow closely its medieval limits." \
#            "The City of Westminster is also an Inner London borough holding city status. " \
#            "Greater London is governed by the Mayor of London and the London Assembly." \
#            "London is located in the southeast of England." \
#            "Westminster is located in London." \
#            "London is the biggest city in Britain. London has a population of 7,172,036."