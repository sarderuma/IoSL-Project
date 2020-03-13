package sender.util;


import java.util.Arrays;
import java.util.Random;
/**
 * A tool class used to generate random byte message given the length.
 * This static getRandomBytes method is used by TrafficGenerator to auto-generate message payload
 * @author Liming Liu
 *
 */
public class RandomByteGenerator {
	
	public static byte[] getRandomBytes(int size) {
		byte[] b = new byte[size];
		new Random().nextBytes(b);
		return b;
	}
	
	//for testing
	public static void main(String args[]) {
	    System.out.println(Arrays.toString(RandomByteGenerator.getRandomBytes(10)));
	}

}
