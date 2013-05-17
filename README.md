/*aTable
======

Multiplication Table Code*/
import java.util.*;

class ATable {

final static int   aTable = 6;

public static void main(String[] args) {

System.out.println( "Multiplication table of " + aTable);
System.out.println();
System.out.println("Multiplier"  +  "   "   +   "Multiplicand" +   "    " + "Result");
int multiplicand = printSixes();
System.out.println();
System.out.println(" End of Table at number " + multiplicand);
}//end of main

private static int printSixes(){

int i = 1;
System.out.println();
while (i *6 < 100) {
 	System.out.println("    6      * "  +   "    "+i+"            =     "    + i*6);
	i++;
}
return i-1;
}// end of function printSixes
}//end of class ATable
	
