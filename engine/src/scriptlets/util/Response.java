package scriptlets.util;

import java.net.HttpURLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class Response {
    private String content = "";
    private HttpURLConnection connection;
    
    public Response(HttpURLConnection connection) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            content = content + "\n" + line;
        }
        reader.close();
    }
    
    public String toString() {
        return content;
    }
    
    public int toInteger() throws IOException {
        return connection.getResponseCode();
    }
}