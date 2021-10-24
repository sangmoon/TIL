import java.util.stream.Stream;

public class LinkedList {

    static class Node {
        private Node next;
        private int val;

        public Node(int val) {
            this.val = val;
        }

        public void setNext(Node next) {
            this.next = next;
        }

        public Node getNext() {
            return next;
        }

        public int getVal() {
            return val;
        }
    }

    public static void main(String[] args) {
        String[] input = {"1","2","3","4","5","6","7"};

        int[] intInput = null;

        try{
            intInput = Stream.of(input).mapToInt(Integer::parseInt).toArray();
        } catch (Exception e) {
            // error 처리
            throw e;
        }

        Node head = new Node(-1);
        Node tail = null;
        Node last = head;

        for(int val: intInput) {
            tail = new Node(val);
            last.setNext(tail);
            last = tail;
        }

        Node printingHead = new Node(-1);
        printingHead.setNext(head.getNext());

        while(printingHead.getNext() != null) {
            System.out.println(printingHead.getNext().getVal());
            printingHead.setNext(printingHead.getNext().getNext());
        }

        Node reverseHead = reverse(head);

        printingHead = reverseHead;
        while (printingHead.getNext() != null) {
            System.out.println(printingHead.getNext().getVal());
            printingHead.setNext(printingHead.getNext().getNext());
        }
    }

    public static Node reverse(Node head) {
        if(head == null || head.getNext() == null) {
            //
        } else {

            head.setNext(innerReverse(head.getNext(), head.getNext().getNext(), true));
        }
        return head;
    }

    public static Node innerReverse(Node pre, Node next, boolean init) {
        if(next == null) {
            return  pre;
        } else {
            if(init) {
                pre.next = null;
            }
            Node nextofNext = next.getNext();
            next.setNext(pre);
            return innerReverse(next, nextofNext, false);
        }
    }
}
