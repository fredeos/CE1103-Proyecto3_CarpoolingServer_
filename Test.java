import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class Test{
    public static void main(String[] args) throws Exception{
        HttpURLConnection connection = (HttpURLConnection) new URL("http://127.0.0.1:8000/askthing").openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Accept", "application/json");

        int responseCode = connection.getResponseCode();
        if(responseCode==200){
            BufferedReader reader =  new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder jsonstring = new StringBuilder();
            String line;
            while((line = reader.readLine())!=null){
                jsonstring.append(line);
            }
            JSONObject json = new JSONObject(jsonstring.toString());
            String message = json.getString("message");
            System.out.println(message);
        }
    }
}