__module_name__ = "Bitlbee Extras"
__module_version__ = "0.1"
__module_description__ = "Some great Bitlbee extras"
__author__ = "Stanislav N. aka pztrn"

import hexchat

# The Help String.
HELP_STR = """\002\00304Bitlbee extras plugin for Hexchat, version %s.\003
Copyright (c) 2017, Stanislav N. aka pztrn <pztrn at pztrn dot name>

This plugin adds some useful features to Hexchat if used with Bitlbee.
\002WARNING:\002 it is required to configure this plugin, otherwise it
will not work!

Commands:

\002/be set [prefname] [value]\002 Sets prefname to value
\002/be set\002                    Lists all parameters set
\002/be get all\002                Lists all parameters available
""" % __module_version__

# Acceptable configuration parameters.
ACCEPTED_PARAMS = {
	"network": "Name of network where Bitlbee Extras will work"
}

# Current configuration
CONFIG = {}

# Processes "be" command.
def be_command(word, word_eol, userdata):
	if len(word) == 4:
		if word[1] == "set":
			be_set(word[2], word[3])
	else:
		if word[1] == "get":
			be_listallparams()
		else:
			be_listprefs()

	return hexchat.EAT_ALL

# List all available parameters with description.
def be_listallparams():
	hexchat.prnt("\002Bitlbee Extras accepts these parameters:\002")
	for item in ACCEPTED_PARAMS:
		hexchat.prnt("\002\00303%s\003\002 - %s" % (item, ACCEPTED_PARAMS[item]))

# List current preferences.
def be_listprefs():
	prefs = hexchat.list_pluginpref()
	hexchat.prnt("\002\00302Bitlbee Extras plugin preferences:\003\002")
	for key in prefs:
		value = hexchat.get_pluginpref(item)
		hexchat.prnt(key + " => " + value)

# Set configuration value.
def be_set(key, value):
	if not key in ACCEPTED_PARAMS.keys():
		hexchat.prnt("\00204Unknown option:\002 %s" % key)
		return

	status = hexchat.set_pluginpref(key, value)
	if status:
		hexchat.prnt("\002\00303Configuration value set: %s => %s\003\002" % (key, value))
		CONFIG[key] = value

# Formats nickname in proper way.
def format_nickname(word, word_eol, userdata):
	if userdata:
		hexchat.prnt(userdata)

	# No nickname in text? Pass.
	if len(word) < 2:
		return hexchat.EAT_NONE

	# Are we selected channel in right network?
	# Requires "network" ocnfiguration parameter to be set.
	netname = hexchat.get_info("network")
		if not "network" in CONFIG.keys() or not CONFIG["network"] or netname.lower() != CONFIG["network"].lower():
			return hexchat.EAT_NONE

	# Get nickname from message.
	nick = word[0]
	# Actual message. Using word_eol here to keep
	# quotes in message
	newmsg = word_eol[0]
	# Get channel from current context.
	channel = hexchat.get_info("channel")
	# Get users for current channel.
	users = hexchat.get_list("users")
	# Find a user.
	newnick = nick
	for u in users:
		if u.nick == str(nick[:-1]):
			if u.host:
				newnick = u.host.split("@")[0]

	if newnick != nick:
		# Get rid of old nick.
		newmsg = " ".join(newmsg.split(" ")[1:])
		newmsg = newnick + ": " + newmsg
		newcmd = "msg " + channel + " " + newmsg
	else:
		newcmd = "msg " + channel + " " + word_eol[0]

	hexchat.command(newcmd)

	return hexchat.EAT_ALL

# Returns help string.
def get_help():
	return HELP_STR

hexchat.hook_command("", format_nickname, priority=hexchat.PRI_HIGHEST)
hexchat.hook_command("be", be_command, help=get_help())

hexchat.prnt("\00303" + __module_name__ + " " + __module_version__ + " successfully loaded.\003")

# Load configuration.
for item in ACCEPTED_PARAMS.keys():
	val = hexchat.get_pluginpref(item)
	if val:
		CONFIG[item] = val

if len(CONFIG) == 0:
	hexchat.prnt("\00304Please see /help be for list of available options and configure this plugin properly!\003")
