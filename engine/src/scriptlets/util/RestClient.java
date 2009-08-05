package scriptlets.util;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.OutputStreamWriter;

import java.util.*;

import scriptlets.util.Response;

public class RestClient {
    public RestClient() {
        
    }
    
    public Response request(String method, String uri, HashMap<String,String> headers, String data) throws IOException, MalformedURLException {
        URL url = new URL(uri);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setDoOutput(true);
        connection.setRequestMethod(method);
        if (method == "POST")
            connection.setInstanceFollowRedirects(false);

        // TODO: Send Headers
        
        if (data != null) {
            OutputStreamWriter writer = new OutputStreamWriter(connection.getOutputStream());
            writer.write(data);
            writer.close();
        }
        
        return new Response(connection);
    }
    
    public Response get(String uri, HashMap headers, String data) throws IOException {
        return request("GET", uri, headers, data);
    }
    public Response get(String uri, HashMap headers) throws IOException { 
        return get(uri, headers, null); 
    }
    public Response get(String uri) throws IOException { 
        return get(uri, null, null); 
    }
    
    public Response post(String uri, String data, HashMap headers) throws IOException {
        return request("POST", uri, headers, data);
    }
    public Response post(String uri, HashMap<String,String> params, HashMap headers) throws IOException {
        String data = "";
        String kvp = "";
        for (String key : params.keySet()) {
            kvp = URLEncoder.encode(key, "UTF-8") + "=" + URLEncoder.encode(params.get(key), "UTF-8");
            data = data + "&" + kvp;
        }
        return post(uri, data, headers);
    }
    public Response post(String uri, String data) throws IOException {
        return post(uri, data, null); 
    }
    public Response post(String uri, HashMap params) throws IOException {
        return post(uri, params, null);
    }
    public Response post(String uri) throws IOException {
        return post(uri, "", null);
    }
    
}