import java.util.Random;
class Quick{
  int cnt;
  int[] A;
  Quick(){
    this.cnt = 0;
  }
  public int[] sortArray(int[] A) {
	  this.A = A;
  	part(0, A.length - 1);
  	return A;
  }
  void part(int from, int to) {
	   if (from + 1 >= to) return;
     // choose random pivot:
     Random generator=new Random();
     int piv = A[from + generator.nextInt(to - from) ];
     
     int i = from - 1, j = to;
     while (true) {
        do {
          cnt++;
          i++; 
        }while (A[i] < piv);
        do {
          cnt++;
          j--; 
        }while (A[j] > piv);
        if (i >= j) break;
        swap(i,j);
        cnt++;
     }
  	part(from, j + 1);
	  part(j + 1, to);
  }
  
  void swap(int i, int j) {
  	int t = A[i];
  	A[i] = A[j];
  	A[j] = t;
  }
}
class Merge {
  int cnt;
  Merge(){
    this.cnt = 0;
  }
  public void sortArray(int[] nums) {
        mergeSort(nums,0,nums.length-1);        
    }
    
    public void mergeSort(int[] nums, int si, int ei)
    {
        if(si<ei)
        {
            int mi = (si+ei)/2;
            mergeSort(nums, si, mi);
            mergeSort(nums, mi+1, ei);
            merge(nums, si, mi, ei);
        }
    }
    
    public void merge(int[] nums, int si, int mi, int ei)
    {
        int a1 = mi-si+1, a2 = ei-mi;
        int[] t1 = new int[a1], t2 = new int[a2];
        for(int i=0; i<a1; i++) t1[i]=nums[si+i];
        for(int i=0; i<a2; i++) t2[i]=nums[mi+1+i];
        int i=0, j=0, k=si;
        while(i<a1 && j<a2)
        {
            cnt++;
            if(t1[i] < t2[j]) nums[k++] = t1[i++];
            else nums[k++] = t2[j++];
        }
        while(i<a1) nums[k++] = t1[i++];
        while(j<a2) nums[k++] = t2[j++];
    }
}
class Mainsort {
  public static void main(String[] args) {
    System.out.println("Hello world!");
    int l = 2;
    while (l <= 20){
      l++;
      int nums[] = new int[l];
      Random generator=new Random();
      for (int i = 0; i < l; i++) {
        nums[i] = generator.nextInt(500);
        System.out.print(String.valueOf(nums[i])+" ");
      }
      System.out.println(" Length:"+String.valueOf(l));
      Quick Q = new Quick();
      for (int b: Q.sortArray(nums.clone()))       
           System.out.print(String.valueOf(b)+" ");
      System.out.println(String.valueOf(Q.cnt)+",");
      //for (int b: nums) System.out.print(String.valueOf(b)+" ");
      Merge M = new Merge();
      M.sortArray(nums);
      
      for (int b: nums) System.out.print(String.valueOf(b)+" ");
      System.out.print(String.valueOf(M.cnt)+",");
      System.out.println(String.valueOf((int)(l*Math.log(l))));
      System.out.println();
    }
  }
}
import java.util.*;

class Main {
  private int[][] A;
  private final int m;
  private final int n;
  private ArrayList<Integer> rX = new ArrayList<>();
  
  public Main(int[][] input ) {
    A = input;  // Set the initial value for the class
    m = A.length;
    n = A[0].length; 
  }
  public void display(String method){
    System.out.println(method);
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++) System.out.print(A[i][j] + " ");
      System.out.println();
    }
    System.out.println("\n");
  }
  public void orderedRows(){
    for (int i = 0; i < m; i++) Arrays.sort(A[i]);
    display("Then Order By Row");
  }
    
  public void initOrderCols(){
    for (int i = 0; i < n; i++){
      for (int j = 0; j < m; j++) rX.add(A[j][i]);
      Collections.sort(rX);
      for (int j = 0; j < m; j++) A[j][i] = rX.get(j);
      rX.clear();
    }
    display("Init Order By Coumn"); 
    orderedRows();
  }

  public void insertOrder(int t){
    for (int i = m-1; i > t; i--) {
      ArrayList<Integer> rY = new ArrayList<>();
      
      for(Integer k : A[i-1]) System.out.print(k+ " ");
      System.out.print("X\n");
      for(Integer k : A[i]) System.out.print(k+ " ");
      System.out.print("Y\n");
      
      int s = 0;
      //int e = n-2;
      for (int j = n-1; j > 0 ; j--){
        if (A[i-1][j] >= A[i][s]) {
          rX.add(A[i][s]);
          rY.add(A[i-1][j]);
          s++;
        }
      }

      for(Integer k : rX) System.out.print(k+ " ");
      System.out.print("rX\n");
      for (Integer k:rY) System.out.print(k+ " ");
      System.out.print("rY\n");

      if (rX.size() > 0) {  // != isEmpty() 
        for (Integer k : A[i-1]) rX.add(k);
        Collections.sort(rX);
        for (int j = s; j < n; j++) rY.add(A[i][j]);
        Collections.sort(rY);
  
        for(Integer k : rX) System.out.print(k+ " ");
        System.out.print("rX\n");
        for (Integer k:rY) System.out.print(k+ " ");
        System.out.print("rY\n");
        
        
        for (int j = 0; j < n; j++){
          A[i-1][j] = rX.get(j);
          A[i][j] = rY.get(j);
        }
        rY.clear();
        rX.clear();
      }
    }
    display("After the Inserts Order " + "--Row:"+ t);
  }

  public int checkEndsOrder(){
    int flag = -1;
    for (int i = 0; i < m-1; i++) {
      for (Integer k : A[i]) rX.add(k);
      if (A[i+1][0] < Collections.max(rX)) flag = i;
      rX.clear();
      //if ((A[i][1] > A[i+1][0]) || (A[i][n-1] > A[i+1][n-2])) flag = true;
    }
    return flag;
  }

  public static void main(String[] args) {
    /* Testing for following 4 test cases */
    //int[][] input = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}};
    //int[][] input = {{8,15,22,0},{3,35,35,15},{7,20,2,10},{30,5,3,9}};
    //int[][] input = {{8,15,22,20},{3,35,35,15},{7,20,2,10},{30,5,3,9}};
    int[][] input = {{5,12,17,21,23},{1,2,4,6,8},{12,14,18,19,27},{3,7,9,15,25}};
    
    Main d2 = new Main(input);
    int times = 0;
    d2.display("Input");
    if (d2.checkEndsOrder() >= 0){
      d2.initOrderCols();
      //d2.orderedRows();
      d2.insertOrder(times); 
    }else System.out.println("Already Sorted");
    times = d2.checkEndsOrder();
    if (times > 0) d2.insertOrder(times);

    //Arrays.sort(A, (a,b) -> Integer.compare(a[i], b[i]));
    //System.out.println("from "+ A[0][0]+"Hello world!" + A[m-1][n-1]); 
  }
}
