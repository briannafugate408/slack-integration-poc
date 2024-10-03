We want to present a viable solution for the GrubHub team to send us orders for their collegiate partners via 
a Slack integration. The solution should provide the provide the GrubHub developers with a webhook that
notifies us in Slack when a new order was submitted to their collegiate software and then that order 
should be funneled down to the makeline. 

In this proof of concept, I have gone through the proper channels of learning how to make a Slack application
that we can send JSON orders to, incorporated our entree-submission tool to hit the partner api entree
endpoint, and lastly, worked with the Slack API to understand how to send orders that we receive to the partner
API to a Slack channel.

How to Run: 
- Run core
- Run machine config server
- Run preprocessor
- Run tracker server
- Run partner api rest server
- Run python server (Slack API)
- Run main python app with `python3 main.py --hmac_secret "yoyoyo" --customer custom --portion_type multiplier`
- Make sure the webhook URL in app is correct for the app you want message sent to
