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

import scriptlets.util.Base64;

public class DispatcherServlet extends HttpServlet {
    public void service(ServletRequest request, ServletResponse response)
            throws ServletException, java.io.IOException {
        
        Hashtable addHeaders = new Hashtable();
        addHeaders.put("RUN_CODE", Base64.encode("resp.write('yo');"));
        HeaderInjectionWrapper modifiedRequest = new HeaderInjectionWrapper((HttpServletRequest)request, addHeaders);
                
        RequestDispatcher dispatcher = getServletContext().getRequestDispatcher("/javascript/");
        dispatcher.forward(modifiedRequest, response);         
    }
}