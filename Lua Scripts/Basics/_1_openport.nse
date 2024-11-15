-- 1. HEAD  (META INFORMATION)
local nmap = require "nmap"
local shortport = require "shortport"
description =[[
  My first ever script in Lua!
]]
author = "boufik"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"safe"}



-- 2. RULE
portrule = function(host, port)
    local port_to_check = {number = 4000, protocol = "tcp" }
    local port_state = nmap.get_port_state(host, port_to_check)
    return port_state ~= nil and port_state.state == "open"
end



-- 3. ACTION
action = function(host, port)
    return "This message will be printed in case port 4000 is open"
end

-- Bash Run: nmap --script my-script-name localhost
