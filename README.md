# Palo-XML-Download

You can backup your palo with Rancid. But without the XMl file you cannot restore your configuration.
With this python script you can download your xml file and it wil cleanup older configs files.

If you cannot reslove the hostname. Then fill the hosts file with IP and Name.

```console
# cat /etc/hosts
1.1.1.1 palo1
1.1.1.2 palo2
```
File the hostname and the [API key](https://docs.paloaltonetworks.com/pan-os/7-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key) in the `paloConfigDownload.conf` file.

You like some slack notification? Change the vars `slackchannel` and `slack_api_token_change_me` with the right info.