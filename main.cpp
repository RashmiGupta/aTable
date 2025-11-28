#include <iostream>
#include <string.h>
 
//Variable Expansion
std::string unalias_env(std::string arg) {
  std::string out = "";
	std::size_t found = arg.find('$');
  
  while(found!=-1) {
      out += arg.substr(0, found);
      if (arg[found+1] == '{') {
        std::size_t end = arg.find('}');
        if (end != -1) {
          std::string envvar = arg.substr(found+2, end-found-2);
          if (const char *envtmp = std::getenv(envvar.c_str())){
                std::string unalias = envtmp;
                out += unalias;
          }else  std::cerr << "error: $" << envvar << " not in environment.\n";     
        }
        arg = arg.substr(end+1,-1);
      }
      
      found = arg.find('$');
    }
    out += arg;
		return out;

int main() {
    int i=system ("echo $?");
    printf ("The value returned was: %d.\n",i);
    std::string arg = "${HOME}p${D}";
    //std::cout << arg << " Hello World!\n";
    if (! (arg.find('$') == -1 && 
      arg.find('{') == -1 && arg.find('}') == -1 ) )
    {
          //std::cout << arg  << " oo\n";
          //std::string envP = unalias_env(arg);
          std::cout << "test"; //envP.c_str() << " oo\n";
    }
  
  	//exp = tilde("~myname/dir");
  	//if (exp) argument = strdup(exp);
    std::cout << "Hello World!\n";
}
`#include <iostream>

#include <httpparser/request.h>
#include <httpparser/httprequestparser.h>

using namespace httpparser;

int main(int, char**)
{
    const char text[] = "GET /uri.cgi HTTP/1.1\r\n"
                        "User-Agent: Mozilla/5.0\r\n"
                        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                        "Host: 127.0.0.1\r\n"
                        "\r\n";

    Request request;
    HttpRequestParser parser;

    HttpRequestParser::ParseResult res = parser.parse(request, text, text + strlen(text));

    if( res == HttpRequestParser::ParsingCompleted )
    {
        std::cout << request.inspect() << std::endl;
        return EXIT_SUCCESS;
    }
    else
    {
        std::cerr << "Parsing failed" << std::endl;
        return EXIT_FAILURE;
    }
}


#include <iostream>

#include <httpparser/response.h>
#include <httpparser/httpresponseparser.h>

using namespace httpparser;

int main(int, char**)
{
    const char text[] =
            "HTTP/1.1 200 OK\r\n"
            "Server: nginx/1.2.1\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: 8\r\n"
            "Connection: keep-alive\r\n"
            "\r\n"
            "<html />";

    Response response;
    HttpResponseParser parser;

    HttpResponseParser::ParseResult res = parser.parse(response, text, text + strlen(text));

    if( res == HttpResponseParser::ParsingCompleted )
    {
        std::cout << response.inspect() << std::endl;
        return EXIT_SUCCESS;
    }
    else
    {
        std::cerr << "Parsing failed" << std::endl;
        return EXIT_FAILURE;
    }
}
#ifndef HTTPPARSER_REQUEST_H
#define HTTPPARSER_REQUEST_H

#include <string>
#include <vector>
#include <sstream>

namespace httpparser
{

struct Request {
    Request()
        : versionMajor(0), versionMinor(0), keepAlive(false)
    {}
    
    struct HeaderItem
    {
        std::string name;
        std::string value;
    };

    std::string method;
    std::string uri;
    int versionMajor;
    int versionMinor;
    std::vector<HeaderItem> headers;
    std::vector<char> content;
    bool keepAlive;

    std::string inspect() const
    {
        std::stringstream stream;
        stream << method << " " << uri << " HTTP/"
               << versionMajor << "." << versionMinor << "\n";

        for(std::vector<Request::HeaderItem>::const_iterator it = headers.begin();
            it != headers.end(); ++it)
        {
            stream << it->name << ": " << it->value << "\n";
        }

        std::string data(content.begin(), content.end());
        stream << data << "\n";
        stream << "+ keep-alive: " << keepAlive << "\n";;
        return stream.str();
    }
};

} // namespace httpparser

extern int main(void);
#endif

#include <iostream>
#include <httpparser/urlparser.h>

using namespace httpparser;

int main(int, char**)
{
    UrlParser parser;

    {
        const char url[] = "git+ssh://example.com/path/file";

        if( parser.parse(url) )
            std::cout << parser.scheme() << "://" << parser.hostname() << std::endl;
        else
            std::cerr << "Can't parse url: " << url << std::endl;
    }

    {
        const char url[] = "https://example.com/path/file";

        if( parser.parse(url) )
            std::cout << parser.scheme() << "://" << parser.hostname() << std::endl;
        else
            std::cerr << "Can't parse url: " << url << std::endl;
    }

    return EXIT_SUCCESS;
}
/*//Makefile
all: main

CXX = g++
override CXXFLAGS += -g -Wno-everything -I./include -L./lib -pthread -lm

SRCS = $(shell find . -name '.ccls-cache' -type d -prune -o -type f -name '*.cpp' -print | sed -e 's/ /\\ /g')
HEADERS = $(shell find . -name '.ccls-cache' -type d -prune -o -type f -name '*.h' -print)

main: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) -O3 $(SRCS) -o "$@"

main-debug: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) -O0 $(SRCS) -o "$@"

clean:
	rm -f main main-debug
  */
