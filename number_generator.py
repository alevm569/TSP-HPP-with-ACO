from collections import deque
import qrng
import random

def q_rng():
    # Con Qiskit
    rnd = qrng.get_random_int(0, 1500)
    return rnd
def rng():
    num = random.randint(0, 1500)
    return num
def generate_number(path_pseudo, path_rand, amount_numbers):
    # PSEUDO
    f_pseudo = open(path_pseudo, 'w')
    print("Pseudo random numbers")
    seed = random.seed(10)
    for i in range(amount_numbers):
        numbers = str(rng()) + '\n'
        f_pseudo.write(numbers)
    f_pseudo.close()
    print("Pseudo random numbers save!")

    # RANDOM
    f_q = open(path_rand, 'w')
    print("Random numbers")
    for k in range(amount_numbers):
        numbers_q = str(q_rng()) + '\n'
        f_q.write(numbers_q)
    f_q.close()
    print("Random numbers save!")
def read_file(path_pseudo, path_rand):
    quantum_list = []
    pseudo_list = []
    f_pseudo = open(path_pseudo, "r")
    f_rand = open(path_rand, "r")
    for linea in f_pseudo:
        linea = linea.strip('\n')
        pseudo_list.append(int(linea))
    for linea in f_rand:
        linea = linea.strip('\n')
        quantum_list.append(int(linea))
    return pseudo_list, quantum_list
def queue_number(list):
    q = deque(list)
    return q
