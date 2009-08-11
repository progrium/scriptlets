package scriptlets.front;

import java.io.IOException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import java.util.*;
import java.io.File;
import java.lang.System;

import scriptlets.util.Base64;
import scriptlets.util.RestClient;

public class DispatcherServlet extends HttpServlet {
    public void service(ServletRequest request, ServletResponse response)
            throws ServletException, java.io.IOException {
        
        String name = (new File(((HttpServletRequest)request).getRequestURI())).getName();
        RestClient client = new RestClient();
        String body = client.get("http://localhost:8081/code/" + name).toString();
        String[] split = body.split("\n", 3);
        String language = split[1].substring(2);
        String code = split[2].trim();
        
        Hashtable addHeaders = new Hashtable();
        addHeaders.put("RUN_CODE", Base64.encode(code));
        HeaderInjectionWrapper modifiedRequest = new HeaderInjectionWrapper((HttpServletRequest)request, addHeaders);
        
        String path = (language.equals("php")) ? "/run.php" : "/" + language + "/";
        RequestDispatcher dispatcher = getServletContext().getRequestDispatcher(path);
        dispatcher.forward(modifiedRequest, response);
    }
}