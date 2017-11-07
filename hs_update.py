import sys, json
from workflow import Workflow, ICON_WEB, web
from apiKey import apiKey

def main(wf):

	if(not apiKey):
		wf.add_item(u'Do you have your API key set?', u'Press Enter to open GitHub for a setup tutorial.', arg='https://github.com/gabrielrios/alfred2-hearthstone/', valid=True, icon='./icon.png')
	else:
		data = web.get('https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1', headers={'X-Mashape-Key': apiKey})
		if(data.status_code != 200):
		    wf.add_item(u'Bad Request. Is your API Key set?', u'Think something should be here that isn\'t? Hit Enter to open an issue on Github', arg='https://github.com/gabrielrios/alfred2-hearthstone/issues/new', valid=True, icon='./icon.png')
		else:
			data = data.json()
			fullCardSet = []
			for cardSet in data:
				fullCardSet += data[cardSet]

			with open('./cards.json', 'w') as outfile:  
			    json.dump(fullCardSet, outfile)
			    wf.add_item(u'Your card list has been updated successfully', u'You can how search using hs Card Name', valid=True, icon='./icon.png')

	wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))