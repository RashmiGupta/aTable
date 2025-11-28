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
class Main {
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
