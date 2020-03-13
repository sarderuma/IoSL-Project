package sender.controller;

import java.util.Timer;
import java.util.TimerTask;

import com.google.common.collect.ImmutableMap;

import io.jaegertracing.internal.JaegerTracer;
import io.opentracing.Scope;
import io.opentracing.propagation.Format;
import io.opentracing.tag.Tags;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import sender.util.RandomByteGenerator;
import sender.util.Tracing;
/**
* The class that sends generated new payload to next hop periodically
*
*/
public class PacketSender {
	
	private int SIZE=0;
	private int FREQ=0;
	private String NEXT_HOP;
	private int PKT_COUNT=0;

	private final OkHttpClient client;
	private Timer timer;
	
	
	public PacketSender(String NEXT_HOP, int SIZE, int FREQ) {
		this.SIZE=SIZE;
		this.FREQ=FREQ;
		this.NEXT_HOP=NEXT_HOP;
		this.client = new OkHttpClient();
	}
	
	public String halt() {
		if(this.timer==null) {
			this.start();
			return "Unexpected case: calling stop before sender starts, will restart sending";
		}
		this.timer.cancel();
		return "halt success";
	}
	
	
	public void start() {
		this.timer=new Timer();
		//define the periodic task
		timer.scheduleAtFixedRate(new TimerTask() {
			@Override
			public void run() {
				try {
					String newMessage = new String(RandomByteGenerator.getRandomBytes(SIZE));

					// each packet will start a new opentracing trace
					PKT_COUNT+=1;
					JaegerTracer tracer = Tracing.init("sender");
					Scope scope = tracer.buildSpan("root span").startActive(false);
					RequestBody requestBody = new MultipartBody.Builder().setType(MultipartBody.FORM)
							.addFormDataPart("message", newMessage).build();
					Request.Builder requestBuilder = new Request.Builder().url(NEXT_HOP).header("Connection",
							"close");
					requestBuilder.post(requestBody);
					scope.span().log(ImmutableMap.of("PacketID", PKT_COUNT));
					Tags.SPAN_KIND.set(tracer.activeSpan(), Tags.SPAN_KIND_CLIENT);
					Tags.HTTP_METHOD.set(tracer.activeSpan(), "POST");
					Tags.HTTP_URL.set(tracer.activeSpan(), NEXT_HOP);
					tracer.inject(tracer.activeSpan().context(), Format.Builtin.HTTP_HEADERS,
							Tracing.requestBuilderCarrier(requestBuilder));

					Request request = requestBuilder.build();
					
					Response response = client.newCall(request).execute();
					scope.span().finish();
					if (response.code() != 200) {
						throw new RuntimeException("Bad HTTP result: " + response);
					}
					System.out.println(response.body().toString());

				} catch (Exception e) {
					e.printStackTrace();
				}

			}
		}, 0, 1000/FREQ);	
	}	
}
