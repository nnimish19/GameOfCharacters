from settings import *

# This method describes user with
    # titles/also_known_as
    # origin
    # allegiance
    # status: he is currently dead
def describe(name):
    response=name
    sub = name.strip().lower().replace(" ","_")

    if sub not in graph: return "Invalid input"

    if ("also_known_as" in graph[sub]):
        response+=", also_known_as " + graph[sub]["also_known_as"][0]
    elif ("titles" in graph[sub]):
        response += ", also_known_as " + graph[sub]["titles"][0]

    if ("origin" in graph[sub]):
        response += ", was born and raised in " + graph[sub]["origin"][0]

    if ("allegiance" in graph[sub]):
        response+= ". "+ sub + " belong to " + graph[sub]["allegiance"][0]

    if ("status" in graph[sub]):
        response += (". "+ sub + " is currently " + graph[sub]["status"][0])

    return response

# This method returns relation between two users.
# if A's rel1 is B, B's rel2 is C. Then A and C are related as -
# A's rel1's rel2's  is C
def relation_bw(sub, obj):
    sub = sub.strip().lower().replace(" ", "_")
    obj = obj.strip().lower().replace(" ", "_")

    if sub not in graph: return "Invalid input"
    if obj not in graph: return "Invalid input"

    path = search_graph(sub,obj)
    if path =={}: return "No relation"

    v = obj
    response = ""
    while (v in path):
        if v == sub: break
        u = path[v][0]
        response = path[v][1] + "'s " + response
        v=u
    return sub+"'s "+ response + "is "+obj

# This method returns A's given relation
# A's father =?, A's children =?
def relation_of(sub, rel):  #relation = ["father","mother","sibling"]
    sub = sub.strip().lower().replace(" ", "_")

    if sub not in graph: return "Invalid input"
    if rel not in link_predicates: return "No relation"
    if rel not in graph[sub]: return "Sorry "+ rel + "'s not in the Database."

    response = graph[sub][rel]
    if len(response)>1: response = sub + " has " + len(response)+ " famously known "+ rel + ". " + " ".join(response)
    else: response = sub + "'s " + rel + ' is ' + response[0]

    return response


# This method returns living status and cause of death of user
def death(sub):
    sub = sub.strip().lower().replace(" ", "_")
    response = ""

    if sub not in graph: return "Invalid input"

    if 'status' in graph[sub]:
        if graph[sub]['status']=='Alive': response = "For God's sake, " + sub +" is still alive!"
        if graph[sub]['status']== 'Uncertain': response = sub + " is likely dead. "
        else: response = sub + " is dead. "
    if 'death' in graph[sub]:
        response += " ".join(graph[sub]['death'])

    return (response if response else (sub+"is likely dead"))


# link_predicates = ['father', 'mother', 'siblings', 'spouse', 'children', 'killer', 'predecessor', 'successor', 'lovers']
def search_graph(src, des):
    path={}
    vis={}

    queue=[src]

    while(queue):
        sub = queue[0]
        del queue[0]
        for pred in link_predicates:
            if pred in graph[sub]:
                for v in graph[sub][pred]:
                    if v in vis: continue
                    vis[v]=1
                    path[v] = [sub,pred]
                    if v == des: return path
                    if v in graph: queue.append(v)

    path = {}
    return path
