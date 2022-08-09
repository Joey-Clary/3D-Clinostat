import websockets.*;

WebsocketServer ws;
int now;
int count = 0;
int old_count = 0;
int failCount = 0;
float x, y;
String old_msg;
PrintWriter output;

String path = "C:/OUTPATH/"; //SET OUTPUT PATH HERE
String name = path + "FILENAME.txt"; //SET OUTPUT FILE NAME HERE 

void setup() {
  size(200, 200);
  ws = new WebsocketServer(this, 8080, "");
   
  output = createWriter(name);
  now=millis();
  x=0;
  y=0;
}

void draw() {
  //Debug display
  ellipse(x, y, 10, 10);
  
  if (millis()>now+1000) {
    if(old_count == count) {
      print("Fail ");
      print(failCount);
      print("/");
      println(count);
      output.print("fail: ");
      output.println(millis());
      output.flush();
      background(random(255), random(255), random(255));
      failCount++;
    }
    else {
      ws.sendMessage("Success");
      old_count = count;
    }
    
    now = millis(); 
  }
}

void webSocketServerEvent(String msg) {
  //Triggered when data received
  //Outputs data to file that can be parsed by python program
  count++;
  println(msg);
  output.println(msg);
  output.flush();
  x=random(width);
  y=random(height);
}
