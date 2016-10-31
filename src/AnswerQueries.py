from GameOfCharacters.src.PrepareRelationGraph import Entity
from GameOfCharacters.src.PrepareRelationGraph import EntityList
from queue import *

#traverse the relation graph using only these edges
relationToVisit = ["father", "mother", "spouse", "children"]

def removeTags(s):
    while True:
        ob=s.find("(")
        cb=s.find(")",ob)
        if ob==-1 or cb==-1:
            break
        s=s[:ob]+s[cb+1:]
    return s

# Removes content within brackets, remove flower brackets and extra spaces    
def filterChildNode(entity):
    entity = entity.lower()
    entity = removeTags(entity)
    loop = True
    while(loop):
        loop = False
        if entity[-1] == ' ':
            entity = entity[0:-1]
            loop = True
        if entity[0] == ' ':
            entity = entity[1:]
            loop = True
        ob=entity.find("{")
        cb=entity.find("}",ob)
        if ob!=-1 and cb!=-1:
            entity=entity[ob+1:cb]
            loop = True
    return entity

#Check if child is biological or adopted child.
def checkAdoptedChild(child, parent):
    rel = ["mother", "father"]
    for s in rel:
        if s in Entity[child]:
            for w in Entity[child][s]:
                if parent in w.lower() and "adopt" not in w.lower() and "legal" not in w.lower():
                    return False
    return True

def bfs(entityOne, entityTwo):
    visited = {}
    prevNode = {}
    visited[entityOne]=True
    q= Queue()
    q.put(entityOne)
    while(q.empty()==False):
        cur=q.get()
        if (cur == entityTwo):
            break
        for s in relationToVisit:
            print(cur+" "+s)
            if s not in Entity[cur]:
                print(s+" not in "+cur)
                continue
            for nextNode in Entity[cur][s]:
                if ("father" == s or "mother" == s) and ("adopt" in nextNode.lower() or "legal" in nextNode.lower()):
                    continue
                nextNode = filterChildNode(nextNode)
                
                if nextNode not in EntityList:
                    for w in EntityList:
                        if w in nextNode:
                            if w in visited:
                                continue
                            if s == "children" and checkAdoptedChild(w, cur):
                                    continue
                            visited[w]=True
                            q.put(w)
                            prevNode[w]=[]
                            prevNode[w].append(cur)
                            prevNode[w].append(s)
                else:
                    if nextNode in visited or (s == "children" and checkAdoptedChild(nextNode, cur)):
                        continue
                    visited[nextNode]=True
                    q.put(nextNode)
                    prevNode[nextNode]=[]
                    prevNode[nextNode].append(cur)
                    prevNode[nextNode].append(s)
    relation = []
    if cur == entityTwo:
        relation.append(cur)
        while(cur != entityOne):
            if "children" in prevNode[cur][1]:
                relation.append("child")
            else:
                relation.append(prevNode[cur][1])
            relation.append(prevNode[cur][0])
            cur = prevNode[cur][0]
        relation.reverse()
    return relation
    
# prints relationship between two entities or prints a relative based on type of query.
#example queries
# Query(2, arya stark, mother) // finds mother of arya stark
# Query(1, arya stark, jon snow) // finds relationship between arya stark and jon snow

def Query(queryType, OrigEntityOne, OrigEntityTwo):
    
    entityOne = OrigEntityOne.lower()
    entityTwo = OrigEntityTwo.lower()
        
    if queryType == "1":
        if entityOne not in Entity:
            print(OrigEntityOne + "is not present in Database\n")
        elif entityTwo not in Entity:
            print(OrigEntityTwo + "is not present in Database\n")
        else:
            print(bfs(entityOne, entityTwo))
    elif queryType == "2":
        if entityOne not in Entity:
            print(OrigEntityOne + "is not present in Database\n")
        elif entityTwo not in Entity[entityOne]:
            print(OrigEntityOne + "does not have " + OrigEntityTwo + "\n")
        else:
            print(Entity[entityOne][entityTwo])