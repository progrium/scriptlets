package scriptlets.front;

import javax.servlet.http.*;
import javax.servlet.*;
import java.util.*;

public class HeaderInjectionWrapper extends HttpServletRequestWrapper
{
    Map headerMap = new Hashtable();
   
    public HeaderInjectionWrapper(HttpServletRequest request, Hashtable injectHeaders)
    {
        super((HttpServletRequest)request);
        for (Enumeration e=request.getHeaderNames();e.hasMoreElements();)
        {
            String key = (String)e.nextElement();
            String value = request.getHeader(key);
            this.headerMap.put(key,value);
        }
        this.headerMap.putAll(injectHeaders);
    }
    
    /**
     * Overriden method from base servlet
     */
    public String getHeader(String name)
    {
       return (String)(headerMap.get(name));
    }
    public java.util.Enumeration getHeaders(String name)
    {
       Vector values = new Vector();
       values.add(getHeader(name));
       return Collections.enumeration(values);
    }
    public java.util.Enumeration getHeaderNames()
    {
       return Collections.enumeration(this.headerMap.keySet());
    }
    public java.util.Map getHeaderMap()
    {
       return this.headerMap;
    }
    
   
}