# Import and initialize the pygame library
import csv
import pygame

csv_file = None

with open('../../output/boards_output.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)