from graph import Graph
from scraper import Scraper
from flask import Flask, jsonify
import logging


logging.basicConfig(filename='test.log', level=logging.DEBUG)
running = True

app = Flask(__name__)
graph = Graph()

while running:
    print "Commands:"
    print "0: quit"
    print "1:(Actor/Movie to parse)"
    print "2:(load graph path)"
    print "3:(execute command)"
    input = raw_input("Command")
    print input
    if input[0] == '0':
        break
    if input[0] == '1':
        test = Scraper('https://en.wikipedia.org/wiki/' + input[2:],  50)
        test.set_speed(1)
        graph = test.begin()
    if input[0] == '2':
        graph.open_json(input[2:])
    if input[0] == '3':
        cmd = "print "
        cmd += input[2:]
        exec(cmd)






'''
test_two = Scraper('https://en.wikipedia.org/wiki/Ryan_Reynolds', 30)
test_two.set_speed(1)

print str(Scraper.get_oldest_actors(graph, 5))

print str(Scraper.get_movies(graph,2009))
print str(Scraper.get_actors(graph,2009))

print Scraper.actor_in(graph,"Chris Bender")
print Scraper.movie_with(graph,"Blade: Trinity")


'''
