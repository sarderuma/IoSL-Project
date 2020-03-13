package sender.util;

import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * A Util class used for sending HTTP messages in a convenient way
 * @author limingliu
 *
 */
public class HttpUtil {
	
	
	public static void send(Socket connection, String message) throws Exception {
		OutputStream out = connection.getOutputStream();
		PrintWriter printwriter=new PrintWriter(out, true);
		printwriter.println(message);
		out.close();
	}
	
	
}
