-- HEAD
local stdnse = require "stdnse"
local shortport = require "shortport"
description = [[
   A simple HTTP scan
]]
author = "boufik"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"safe"}


-- RULES
portrule = shortport.port_or_service(8000, "http-alt")


-- ACTION
action = function(host, port)
    return port.version.name .. " is " .. port.state .. " and running on port number " .. port.number .. "."
end


-- Bash Run: nmap --script my-script-name localhost
