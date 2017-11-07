import sys
from workflow import Workflow, ICON_WEB, web

def main(wf):

	args = wf.args

	if len(args):
	    query = args[0]
	else:
	    query = ''

	if(len(query) < 10):
		wf.add_item(u'Press Enter to open hearthstoneapi.', u'Sign up for an account to get an API Key. Come back and paste that key here.', arg='https://market.mashape.com/omgvamp/hearthstone', valid=True, icon='./icon.png')
	else:
		wf.add_item(u'Set API key as: ' + query, arg=query, valid=True, icon='./icon.png')

	wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))