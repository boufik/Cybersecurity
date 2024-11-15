-- HEAD
local shortport = require "shortport"
description = [[
    A simple script
]]
author = "boufik"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"safe"}
 
 
-- RULES
portrule = shortport.port_or_service(80, "http")
 
 
-- ACTION
action = function(host, port)
    return "This message is shown, because my script identified an " .. port.state .. " port (" .. port.number .. ") running " .. port.version.name
end
 
-- Bash Run: 6 comma-separated scripts without spacebar!
-- nmap --script http-title,http-enum,http-csrf,ssh-hostkey,ssh-auth-methods,my-script-name scanme.nmap.org
