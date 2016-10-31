import re

EntityStartSeq = "<<<<<"
AttributeStartSeq = "<<<"

# Stores information regarding each character/place
#Its a 2D dictionary pointing to a List
Entity = {}

#Used to store all the characters/places
EntityList = []

# Add node to relationship graph
def AddNewEntity(entity):
    if entity in EntityList:
        return 1
    EntityList.append(entity)
    Entity[entity] = {}
    #print(entity)
    return 0

# Add edges to a node in Relationship Graph
def AddValuesToEntity(entity, attributes):
    if entity not in Entity:
        return 1
    
    Entity[entity][attributes[0].lower()]=[]
    for i in range(1,len(attributes)):
        Entity[entity][attributes[0].lower()].append(attributes[i][1:])
    #    print("Added "+attributes[i]+" to "+entity)

    return 0
#...
#This function removes content within brackets
#...
def removeTags(s):
    while True:
        ob=s.find("(")
        cb=s.find(")",ob)
        if ob==-1 or cb==-1:
            break
        s=s[:ob]+s[cb+1:]
    return s

# Removes content within brackets and extra spaces    
def filterEntity(entity):
    entity = entity.lower()
    entity = removeTags(entity)
    if entity[-1] == ' ':
        entity = entity[0:-1]
    if entity[0] == ' ':
        entity = entity[1:]
    return entity

# Prepare graph    
def PrepareGraph():
    f = open('../Data/CollectedData.txt', 'r')
    splitter=re.compile(AttributeStartSeq)
    entity = ""
    for line in f:
        line = line[0:-1]
        if len(line) < 3:
            continue
        if EntityStartSeq in line:
            
            entity = filterEntity(line[len(EntityStartSeq)+1:])
            if AddNewEntity(entity) == 1:
                print("Entity already added"+line)
            #else:
            #    print("Entity added "+entity)
        elif AttributeStartSeq in line:
            tmp = [s for s in splitter.split(line) if s!='' and s!=' ']
            if AddValuesToEntity(entity, tmp) == 1:
                print("Attributes addition failed "+line)
        else:
            print("Error at Line:"+line)