package sender.main;

import sender.controller.TriggerListener;

/**
 * Launcher of a new sender instance
 * @author Liming Liu
 *
 */
public class SenderLauncher {
	
	private static String NEXT_HOP;
	private static int FREQ;
	private static int SIZE;
	private static final int TRIGGER_LISTENING_PORT=80;
	private static final int NEXT_HOP_PORT=5000;
	
	public static void main(String[] args) {
		
		//read parameters from container environment
		try {
			NEXT_HOP="http://"+System.getenv("NEXT_HOP")+":"+NEXT_HOP_PORT;
			FREQ = Integer.parseInt(System.getenv("FREQ"));
			SIZE=Integer.parseInt(System.getenv("SIZE"));
			if(FREQ<1||SIZE<1) {
				System.out.println("Frequency or size parameters less than 1, please check again!");
				System.out.println("Frequency: "+FREQ);
				System.out.println("Packet size: "+SIZE);
				return;
			}
		} catch (NumberFormatException e) {
			e.printStackTrace();
		}
		System.out.println("Send to next hop: "+NEXT_HOP);
		System.out.println("Frequency: "+FREQ);
		System.out.println("Packet size: "+SIZE);

		//start new server by read-in parameters
		TriggerListener newServer=new TriggerListener(TRIGGER_LISTENING_PORT,NEXT_HOP,FREQ,SIZE);
		newServer.start();
	}
	
	
}
