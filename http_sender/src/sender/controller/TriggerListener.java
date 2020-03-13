package sender.controller;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

import sender.util.HttpUtil;

/**
 * A web server that 
 * @author limingliu
 *
 */
public class TriggerListener {

	private static final Logger logger = Logger.getLogger("SENDER");
	
	private int TRIGGER_LISTENING_PORT;
	private String NEXT_HOP;
	private int FREQ=0;
	private int SIZE=0;
	private int actionTrigger;
	private final int STATUS_INIT=0;
	private final int STATUS_SENDING=1;
	private final int STATUS_HALT=2;
	
	
	public TriggerListener(int port,
			String destinationAddress, int frequency, int size) {
		this.TRIGGER_LISTENING_PORT=port;
		this.NEXT_HOP=destinationAddress;
		this.FREQ=frequency;
		this.SIZE=size;
		this.actionTrigger=0;
	}
	

	public void start() {
		//start listening for trigger packet
		
		PacketSender ps= new PacketSender(NEXT_HOP, SIZE, FREQ);
		
		try (ServerSocket server = new ServerSocket(this.TRIGGER_LISTENING_PORT)) {
			
			logger.info("Accepting connections on port " + server.getLocalPort());
			
			//remains idle until hears first trigger message, then start sending packets to next hop. if second trigger message arrives stop sending
			while (true) {
				Socket connection=null;
				try {
					connection = server.accept();
					logger.info("Received trigger");
					if(actionTrigger==STATUS_INIT) {
						HttpUtil.send(connection, "HTTP/1.0 200 OK\r\n\r\n");
						ps.start();
						logger.info("Start sending packets");
						actionTrigger=STATUS_SENDING;
						continue;
					}
					if(actionTrigger==STATUS_SENDING) {
						HttpUtil.send(connection, "HTTP/1.0 200 OK\r\n\r\n");
						logger.info(ps.halt());
						actionTrigger=STATUS_HALT;
						continue;
					}
					if(actionTrigger==STATUS_HALT) {
						HttpUtil.send(connection, "HTTP/1.0 200 OK\r\n\r\n");
						ps.start();
						logger.info("Start sending packets");
						actionTrigger=STATUS_SENDING;
						continue;
					}
				} catch (IOException ex) {
					logger.log(Level.WARNING, "Exception accepting connection", ex);
				} catch (RuntimeException ex) {
					logger.log(Level.SEVERE, "Unexpected error", ex);
				} finally {
					connection.close();
				}
			}
			
			
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
}