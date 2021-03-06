#!/usr/bin/env python
# -*- coding: utf-8 -*-

city_name = "São Paulo"

#################################

import hashlib
import binascii
import time
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.edam.notestore.ttypes import NoteFilter
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

# Sandbox: https://sandbox.evernote.com/api/DeveloperToken.action
# Production: https://www.evernote.com/api/DeveloperToken.action
auth_token = "S=s1:U=8f65c:E=14fa7113473:C=1484f600570:P=1cd:A=en-devtoken:V=2:H=484744fd0ffa906797416ae02ce5cd9c"

client = EvernoteClient(token=auth_token, sandbox=True)

note_store = client.get_note_store()

# Listar todos notebooks:
notebooks = note_store.listNotebooks()
# print "Achei ", len(notebooks), " notebooks:"
# for notebook in notebooks:
    # print "  * ", notebook.name

# Criar uma nova nota:
# print "\nCriando uma nova nota no notebook principal\n"

note = Types.Note()
note.title = "Business Travel to %s" % (city_name)

# Anexando uma imagem:
image = open('SP.png', 'rb').read()

md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

# Adicionando o novo Resource na lista de resources dessa nota
note.resources = [resource]

# Para exibir a imagem no meio da nota, soh precisamos do hash MD5 dela
hash_hex = binascii.hexlify(hash)

# ENML = Evernote Markup Language. It's an HTML subset with some extra tags
# note.content = '<?xml version="1.0" encoding="UTF-8"?>'
# note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
# note.content += '<en-note>'
# note.content += 'Esta eh uma nova nota, inserida direto no notebook principal :)<br/>'
# note.content += 'Olha aqui o logo do Evernote:<br/>'
# note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
# note.content += '</en-note>'

flight_bool, history_bool, taxi_bool, hotel_bool, weather_bool, tip_bool = True, True, True, True, True, True

note.content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
    <div>
    	"""
if flight_bool:
    note.content += """
        <div>
            <ul><li><strong>Flight</strong></li></ul>
        </div>
        <div>SFO -&gt; GRU</div>
        <div><en-todo/> arrive on SFO by 4:20pm</div>
        <div><en-todo/> use gate 13</div>
        <div><en-todo/> takeoff is at 7:20pm</div>
        <hr></hr>
		"""
###
if history_bool:
    note.content += """
        <div>
            <ul><li><strong>History</strong></li></ul>
        </div>
        <div>The last time you've been there was on February 02, 2014 - February 10, 2014</div>
        <hr></hr>
        """
###
if taxi_bool:
    note.content += """
        <div>
            <ul><li><strong>Taxi</strong></li></ul>
        </div>
        <div>The last time you've been there you used 03 taxi cabs.</div>
        <div><en-todo/> Download <a href="http://www.easytaxi.com/">EasyTaxi</a> (it works the best in """+ city_name +""")</div>
        <hr></hr>
        """
###
if hotel_bool:
    note.content += """
        <div>
            <ul><li><strong>Hotel</strong></li></ul>
        </div>
        <div>You're staying at:</div>
        <div>Hotel XYZ</div>
        <div>123 something st</div>
        <div>
            <a href="tel:+1(415)555-1234">+1(415)555-1234</a>
        </div>
        <div><en-todo/> check in at hotel</div>
        <hr></hr>
        """
###
if weather_bool:
    note.content += """
        <div>
            <ul><li><strong>Weather</strong></li></ul>
        </div>
        <div>It'll be summertime in """+ city_name +"""</div>
        <div><en-todo/> Grab a coat, it'll be rainy</div>
        <hr></hr>
        """
###
def get_tip_notes(start_date, end_date):
	tip_notes = []

	noteFilter = NoteFilter()
	noteFilter.words = "tag:tip created:%s -created:%s" % (start_date, end_date) # notes with tag #tip created between 2012-01-01 and 2014-09-08 (flight dates)
	note_list = note_store.findNotes(auth_token, noteFilter, 0, 10)

	for note in note_list.notes:
		guid = note.guid
		title = note.title
		user_id = "587356"
		shard_id = "s1"
		url = "evernote:///view/%s/%s/%s/%s/" % (user_id, shard_id, guid, guid)
		tip_notes.append( '<div><en-todo/> %s (<a href="%s">view full note</a>)</div>' % (title, url) )
	return tip_notes

if tip_bool:
    note.content += """
        <div>
            <ul><li><strong>#tip</strong></li></ul>
        </div>
        <div>When you last visited there, you wrote the following #tip:</div>"""
    tip_notes = get_tip_notes("20120101", "20140908")
    for tip_note in tip_notes:
    	note.content += tip_note
    note.content += """
        <hr></hr>
        """
###
note.content += """
    </div>
    """
note.content += """
    <div>
        <br clear="none"/>
        <en-media type="image/png" hash="%s"/>
    </div>
</en-note>""" % (hash_hex)

# Set our beloved bizmem tag :)
note.tagNames = ["bizmem"]

# Set the reminder
# for demo purposes, we'll ignore the actual useful reminder date (two days before the flight) and set it to today
now = int(round(time.time() * 1000)) 
then = now + 60*60*1000 # one hour after `now`
 
# init NoteAttributes instance
note.attributes = Types.NoteAttributes()
note.attributes.reminderOrder = now
note.attributes.reminderTime = then


# Finally, save the note
created_note = note_store.createNote(note)

print "Note created successfully! GUID: ", created_note.guid