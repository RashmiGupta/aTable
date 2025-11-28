class LMS {
    String Data_item_name;
    bool LOCK;
    int Locking_transaction;
    Queue<Integer> waiting_transactions;
    public  L(String item, bool state){
      this.Data_item_name = item;
      this.LOCK = state;
      this.waiting_transactions = new Queue<Integer>();
    }
    public  int getLocking_Transaction(){ return this.Locking_transaction; }
    public  void setLocking_Transaction(int tID){ this.Locking_transaction = tID; }
    public bool isWaiting() {
      if (waiting_trasactions.isEmpty()) return false;
      else return true;
    }
    public int getWaitingT() {
      LOCK.state = false;
      setLocking_Transaction(waiting_trasactions.pop());  }   
}
class Main {
  HashMap<String, L> lock_table = new HashMap<>();
  public static void lock_item( LMS X) {
    while (true)
        if (X.LOCK == false) {	  //item is unlocked 
            X.LOCK = true; 	    //lock the item 
            break;
        } else while (L.LOCK(X) == true) sleep(1); 
  } // until item unlocked and lock manager wakes up the transaction)   
  public static void unlock_item(LMS X) {
      X.LOCK = false; 	     //unlock  item 
      if ( X.isWaiting() == true )
        X.getWaitingT();     
  } //wakeup one of the waiting
  public static void main(String[] args) {
    System.out.println("Hello world!");
  }
}
