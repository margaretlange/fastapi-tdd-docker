at the moment /init-letsencrypt.sh seems to do the trick. the config is intense and I only got it workign by starting with the github repo and going from there bit by bit.
https://github.com/wmnnd/nginx-certbot
https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71

then
docker-compose -f docker-compose-get-key.yml down
docker-compose -f docker-compose-api-only.yml up
then ping and docs should both work at mmldemo.com, http://mmldemo.com and https://mmldemo.com

try out dummy react front end finally
docker-compose -f docker-compose-api-only.yml down 
docker-compose -f docker-compose-prod.yml down 



ec2 looking at the folder learning-terraform-aws-instance
https://dev.to/sre_panchanan/introduction-to-aws-s3-remote-backend-with-terraform-28i7

starting with create_terraform_backend as its own folder put this in gitlab?

install docker
sudo apt-get install docker

sudo service docker start

Testing sql connectivity



ssl
https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
https://aws.amazon.com/getting-started/hands-on/get-a-domain/

Register Domain Name Route 53

When you register a domain, we automatically create a hosted zone that has the same name as the domain. You use the hosted zone to specify where you want Amazon Route 53 to route traffic for your domain. The fee for a hosted zone is $0.50 per month. You can delete the hosted zone if you want to avoid this charge. See the Amazon Route 53 Hosted Zone pricing documentation for full details.

Using us-west-2

Nginx
https://geshan.com.np/blog/2024/03/nginx-docker-compose/
https://geekflare.com/dev/nginx-static-files-node-js/
https://medium.com/@olawalekareemdev/multi-containarized-react-appliation-with-nginx-as-a-reverse-proxy-using-docker-compose-f46691b4d5ad


step one:
buy domain
setup nginx front end to work locally without ssl or certification
what is a dns record??
what is this classic load balancer??

https://aws.amazon.com/getting-started/hands-on/get-a-domain/
i don't want a classic load balancer just an ec2 instance

i have my ec2 instance running docker-compose etc

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html
see if i can do this with terraform

://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record

https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
