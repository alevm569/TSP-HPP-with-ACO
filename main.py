import random
import numpy as np
import qrng
#import quantumrandom
from matplotlib import pyplot as plt

def q_rng():
    # Con Qiskit
    rnd = qrng.get_random_float(0, 1) #random bit float 0 y 1 of 32 bits
    return rnd
def rng(seed):
    random.seed(seed)
    num = random.random() #entre 0,0 y 1,0
    return num
def generate_number(path_pseudo, path_rand, amount_numbers):
    #PSEUDO
    f_pseudo = open(path_pseudo, 'w')
    print("Pseudo random numbers")
    for k in range(amount_numbers):
        seed = random.randint(0, 1000)
        numbers = str(seed) + ',' + str(rng(seed)) + '\n'
        f_pseudo.write(numbers)
    f_pseudo.close()
    print("Pseudo random numbers save!")
    #RANDOM
    f_q = open(path_rand, 'w')
    print("Random numbers")
    print("Connect to IBMQ")
    # Usar en caso de generar un nuevo token para actualizarlo en el disco
    # IBMQ.save_account('46d750be93a92ced7fce989ae6af269098f2f051ab76accf9882d6ea8483cebca9c2e5a7069db5f16e950654c9e67f463a5e95aeb7a19200579df1adac8a4461', overwrite=True)
    # Conexion de la cuenta de IMBQ con qrng (generador de numeros cuanticos de codigo abierto)
    qrng.set_provider_as_IBMQ(
        '46d750be93a92ced7fce989ae6af269098f2f051ab76accf9882d6ea8483cebca9c2e5a7069db5f16e950654c9e67f463a5e95aeb7a19200579df1adac8a4461')
    qrng.set_backend('ibmq_quito')  # conectado al computador cuantico 'ibmq_quito' que tiene 5 qubits

    for k in range(amount_numbers):
        numbers_q = str(q_rng())+'\n'
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
        l_final = linea.split(',')
        pseudo_list.append(float(l_final[1]))
    for linea in f_rand:
        linea = linea.strip('\n')
        quantum_list.append(float(linea))
    return pseudo_list, quantum_list
def plot_numbers(lists):
    print("Plot pseudo random numbers")
    pseudo_list, quantum_list = lists
    plt.hist(np.asarray(pseudo_list, dtype='float'), bins=10, color='#F2AB6D', rwidth=0.85)
    plt.ylabel('Frecuencia')
    plt.xlabel('Pseudo random numbers')
    plt.title('Histograma de pseudo random numbers')
    plt.savefig('pseudo_random_numbers' + '.png')

    plt.show()

    print("Plot random numbers")
    plt.hist(np.asarray(quantum_list, dtype='float'), bins=10, color='#F2AB6D', rwidth=0.85)
    plt.ylabel('Frecuencia')
    plt.xlabel('Quantum random numbers')
    plt.title('Histograma de quantum random numbers')
    plt.savefig('random_numbers' + '.png')
    plt.show()
if __name__ == '__main__':
    path_pseudo = "pseudo_random/pa_numbers.txt"
    path_rand = "random/q_numbers.txt"
    amount_numbers = 10000
    print("Generating numbers")
    generate_number(path_pseudo, path_rand,amount_numbers)
    lists = read_file(path_pseudo, path_rand)
    plot_numbers(lists)


