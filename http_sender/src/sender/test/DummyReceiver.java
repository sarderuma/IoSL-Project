package sender.test;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 * The dummy receiver used for testing sender
 * @author Liming Liu
 *
 */
public class DummyReceiver {

	
	private static final Logger logger = Logger.getLogger("ReceiverServer");
	private final int port;
	
	//main function
	public static void main(String args[])
	{
		//configure the receiver's port number
		int port=5000;
		DummyReceiver rs=new DummyReceiver(port);
		rs.start();
	}
	
	public DummyReceiver(int port) {
		this.port=port;
	}
	
	//start http server
	public void start() {
		
		ExecutorService pool = Executors.newFixedThreadPool(100);
		
		try (ServerSocket server = new ServerSocket(this.port)) {
			logger.info("Accepting connections on port " + server.getLocalPort());
			while (true) {
				try {
					Socket connection = server.accept();
					pool.submit(new HTTPRequestHandler(connection));
				} catch (IOException ex) {
					logger.log(Level.WARNING, "Exception accepting connection", ex);
				} catch (RuntimeException ex) {
					logger.log(Level.SEVERE, "Unexpected error", ex);
				}
			}
		} catch (IOException ex) {
			logger.log(Level.SEVERE, "Could not start server", ex);
		}
		
	}
		
	//the reqest handler that prints out the request message from sender and send HTTP 200OK back
	private class HTTPRequestHandler implements Callable<Void> {
		
		private final Socket connection;
		
		HTTPRequestHandler(Socket connection) {
			this.connection = connection;
		}
		
		//read message and return 200 ok code
		@Override
		public Void call() throws IOException {
			try {
				
				BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
				OutputStream out = new BufferedOutputStream(
						connection.getOutputStream());
				
				//read request
				String line;
				StringBuilder request=new StringBuilder();
				int flag=0;
		        while ((line = in.readLine()) != null) {
		          if (line.length() == 0)
		          {
		        	  if(flag==0) {
		        		  flag=1;
		        	  }
		        	  else {
		        		  break;
		        	  }
		          }
		          request.append(line+"\n");
		        }
		        System.out.println(request.toString());
				
		       //send response
		       String responseString=new String("HTTP/1.0 200 OK\r\n\r\n");
		       byte[] responseBytes=responseString.getBytes();
		        out.write(responseBytes);
		        out.flush();
		        
			} catch (IOException ex) {
				logger.log(Level.WARNING, "Error writing to client", ex);
			} finally {
				connection.close();
			}
			return null;
		}
	}
}
