import serial                                           
import matplotlib.pyplot as plt
import matplotlib.animation as anm

def read_serial_data(port):
    return port.readline().decode().strip('\s\n\r').split('\t')

with serial.Serial(port='COM5', baudrate=115200, timeout=1) as port:

    port.write('b'.encode())

    #port.write(input().encode())

    #while True:
    #    print(read_serial_data(port))

    fig = plt.figure()
    tensaox = fig.add_subplot(2,2,1)
    correntex = fig.add_subplot(2,2,2)
    temperaturax = fig.add_subplot(2,2,3)
    iluminanciax = fig.add_subplot(2,2,4)

    x = [0]

    tensaoy = [0]
    correntey = [0]
    temperaturay = [0]
    iluminanciay = [0]

    def update(frame):
        n = len(x)
        x.append(x[-1] + 1)
        data = read_serial_data(port)
        tensaoy.append(data[0])
        correntey.append(data[1])
        temperaturay.append(data[2])
        iluminanciay.append(data[3])

        n += 1
    
        tensaox.set_xlim(-50+n, n)
        correntex.set_xlim(-50+n, n)
        temperaturax.set_xlim(-50+n, n)
        iluminanciax.set_xlim(-50+n, n)

        tensaox.plot(x, tensaoy, '-', color='blue')
        correntex.plot(x, correntey, '-', color='red')
        temperaturax.plot(x, temperaturay, '-', color='green')
        iluminanciax.plot(x, iluminanciay, '-', color='orange')

        fig.gca().relim()
        fig.gca().autoscale_view() 

        port.write('b'.encode())


    animation = anm.FuncAnimation(fig, update, interval=50)
    plt.show()