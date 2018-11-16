# -*- coding: utf-8 -*-

def clear_content(contents, seperator='\r\n'):
    return seperator.join([''.join(c.split()) for c in contents if len(c.strip()) > 0])