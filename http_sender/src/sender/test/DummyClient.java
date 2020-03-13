package sender.test;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
/**
 * A dummy web client used to test action trigger.
 * This client will send a simple HTTP/GET request to the sender's server, then the sender will start/stop sending packets
 * This class is only used for testing
 * @author Liming Liu
 *
 */
public class DummyClient {
	
		//configure sender server address
		private static String senderServerAddress="http://localhost:3000";

		private URL url;

		//test message, can be anything		
		private static String message="";
		
		public DummyClient (URL url,String message) {
			if (!url.getProtocol().toLowerCase().startsWith("http")) {
				throw new IllegalArgumentException("Posting only works for http URLs");
			}
			this.url = url;
			this.message=message;
		}
		
		//send the trigger request 
		public InputStream sendTriggerMessage() throws IOException {
			URLConnection uc = url.openConnection();
			uc.setDoOutput(true);
			try (OutputStreamWriter out
					= new OutputStreamWriter(uc.getOutputStream(), "UTF-8")) {
		
				try {
					out.write(message);
					out.write("\n");
					out.write("\n");
					out.flush();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			return uc.getInputStream();
		}
		
		//main function
		public static void main(String args[]) {
			try {
				URL url=new URL(senderServerAddress);
				DummyClient newDummy=new DummyClient(url, message);
				try {
					newDummy.sendTriggerMessage();
				} catch (IOException e) {
					e.printStackTrace();
				}
				
			} catch (MalformedURLException e) {
				e.printStackTrace();
			}
			
			
		}
}
