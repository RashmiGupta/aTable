

import static java.awt.Color.*;
import java.awt.Color;
import java.awt.Dimension;
import static java.awt.EventQueue.invokeLater;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.SwingUtilities;
import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JLayeredPane;
import static javax.swing.JLayeredPane.DEFAULT_LAYER;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.LineBorder;
import javax.swing.event.MouseInputAdapter;

public class Grid{
  final static int 
      GRID_PANEL_BORDER_WIDTH = 5,
      N = 15,
      CELLSIZE = 20;

  static final JPanel panel = new JPanel();
  static final int SM_CELL_BORDER_WIDTH = 1;
  static LineBorder SMcellBorder = new LineBorder(BLACK,SM_CELL_BORDER_WIDTH);

  static JTextField[][] cells = new JTextField[N][N];

  static JFrame frame = new JFrame();

  // Constructor
  public Main(){
    makeGrid();
  }

  private void makeGrid(){ 
    JPanel pnlGrid = new JPanel();
    pnlGrid.setLayout(new GridLayout(N,N));
    pnlGrid.setBackground(BLUE);
    pnlGrid.setBorder(BorderFactory.createLineBorder(Color.red,GRID_PANEL_BORDER_WIDTH));
    pnlGrid.setLayout(new GridLayout(N, N));
 
   /* MouseListener mouseHandler=new MouseAdapter()   {
            @Override
            public void mousePressed(MouseEvent e) {
                doMousePressed(e);
            }
    };*/
    for(int i = 0 ; i < N ; i++)
      for(int j = 0; j < N; j++){
        cells[i][j] = new JTextField();
        cells[i][j].setText(" ");
        cells[i][j].setPreferredSize(new Dimension(CELLSIZE,CELLSIZE));
        cells[i][j].setHorizontalAlignment(JTextField.CENTER);
        cells[i][j].setFocusTraversalKeysEnabled(false);
        cells[i][j].setBorder(SMcellBorder);
        cells[i][j].setOpaque(true);
        pnlGrid.add(cells[i][j]);
    }

    pnlGrid.setPreferredSize(new Dimension(N*(CELLSIZE + 1) + 2*GRID_PANEL_BORDER_WIDTH , 
                                           N*(CELLSIZE + 1) + 2*GRID_PANEL_BORDER_WIDTH));
    panel.add(pnlGrid);
    panel.setVisible(true);
    panel.setOpaque(true);
    panel.setPreferredSize(pnlGrid.getPreferredSize());
    panel.setVisible(true);
    frame.add(panel);
    frame.setSize(new Dimension(pnlGrid.getPreferredSize()));
    frame.setVisible(true);
    frame.pack();
  }

  /*public void doMousePressed(MouseEvent e) {
     Point p = e.getPoint();
     System.out.println("Source point = " + p + " within " + e.getComponent());
     p = SwingUtilities.convertPoint(e.getComponent(), p, e.getComponent().getParent());
        System.out.println("Converted point = " + p + " within " + e.getComponent().getParent());
  }*/


  public static void main(String[] args) {
    invokeLater(new Runnable() {
      public void run() {
        new Grid();
      }
    });
  }

}
