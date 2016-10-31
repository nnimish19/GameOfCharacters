from GameOfCharacters.src.PrepareRelationGraph import *
from GameOfCharacters.src.AnswerQueries import Query
from GameOfCharacters.src.CollectLinks import *
from GameOfCharacters.src.CollectData import *

def main():
    #spider("http://www.gameofthrones.wikia.com/wiki/Category:Characters", 1000)
    #StartDataCollection()
    PrepareGraph()
    while(True):
        ty = input("Enter type")
        if ty == '0':
            break;
        en1 = input("enter entity one")
        en2 = input("entity two")
        Query(ty, en1, en2)