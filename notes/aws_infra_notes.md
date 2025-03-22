eip is elastic ip resource

hosted zone needed to look it up
"/hostedzone/Z05594464A8NYVR2AVJ3" 

route 53 is a DNS system?
aws route53 get-hosted-zone --id /hostedzone/Z05594464A8NYVR2AVJ3
aws route53domains list-domains
isn't working (last invocation)


How to delete manually (annoying):
delete instance
dissociate elastic ip
release elastic ip
delete records in hosted zone
delete hosted zone
delete rds
delete rds network interface
delete security groups in order

keeping mmldemo.com though
