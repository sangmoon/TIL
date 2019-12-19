class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None for i in range(size)]
        self.front = self.rear = -1

    def enqueue(self, data):
        """
        add an element into the queue
        """

        # if queue if full
        if((self.rear + 1) % self.size == self.front):
            print("queue is Full")
        # if queue is empty
        elif(self.front == -1):
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = data
        # else
        else:
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data

    def dequeue(self):
        """
        get an element from the queue
        """
        # if queue is empty
        if(self.front == -1):
            print("queue is Empty!")

        # if queue has only 1
        elif(self.front == self.rear):
            data = self.queue[self.front]
            self.front = -1
            self.rear = -1
            return data

        # else
        else:
            data = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return data

    def show(self):
        """
        display elements in the queue
        """
        # condition for empty queue
        if(self.front == -1):
            print("Queue is Empty")

        elif (self.rear >= self.front):
            print("Elements in the circular queue are:")
            for i in range(self.front, self.rear + 1):
                print(self.queue[i],)
        else:
            print("Elements in Circular Queue are:")
            for i in range(self.front, self.size):
                print(self.queue[i])
            for i in range(0, self.rear + 1):
                print(self.queue[i])
        if ((self.rear + 1) % self.size == self.front):
            print("Queue is Full")


if __name__ == "__main__":
    ob = CircularQueue(5)
    ob.enqueue(14)
    ob.enqueue(22)
    ob.enqueue(13)
    ob.enqueue(-6)
    ob.show()
    print("Deleted value = ", ob.dequeue())
    print("Deleted value = ", ob.dequeue())
    ob.show()
    ob.enqueue(9)
    ob.enqueue(20)
    ob.enqueue(5)
    ob.show()
