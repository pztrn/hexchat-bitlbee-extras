# Hexchat Bitlbee Extras.

This repository contains Hexchat plugin which should make your life
with Bitlbee much easier and nicer.

# Installation

Grab ``bitlbee_extras.py``, put into ``~/.config/hexchat/addons`` and
load it.

# Configuration

## Bitlbee

Make sure you have:

```
nick_format = %full_name
```

in global or account-specific configuration.

## Plugin

Plugin can be configured, see ``/help be`` and ``/be get all`` after
plugin loading.

**WARNING:** Plugin will not work until you do:

```
/be set network NETNAME
```

Where ``NETNAME`` is a name of Bitlbee network. If you have it multiworded
(e.g. "ZNC - Bitlbee") - just put them in quotes like:

```
/be set network "ZNC - Bitlbee"
```

# What it do

This is a list of functions it executes:

* Automatically replaces bad XMPP MUC (and possibly other) nicknames with
valid ones (taken from userhost).
