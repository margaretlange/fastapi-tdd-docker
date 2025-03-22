# How to provision infrastructure for the REST api and react frontend stub
- Note: Hopefully this isn't overkill. The more automated the better for a startup, I think. At least that was my experience at my last job.


### Repositories
- Terraform
  - aws backends for storing state
  - aws main for infrastructure
  - auth0

### Accounts needed
- Amazon web services account (for basic infrastructure including server and database)
	- note to self: set up with the root account right now but not ideal
        - you will need to link payment for registration of a domain ($10?)
        - registering your domain with amazon is the easiest way to automate the whole process
- google developer account (for setting up social authentication via google)
- github account (for accessing the repositories *and* for setting up social authentication for the app via github)
- auth0 account (for setting up app authentication system)
   

### Clients and Installations
- install terraform. I tested my infrastructure code using version 1.11.2, the latest version as of March 21, 2025.
  - https://developer.hashicorp.com/terraform/install
- install and configure the aws client using your aws identity

## Set up terraform backends using Terraform 

## Install aws infrastructure with terraform
- create a local ssh key


## Install auth0 dependencies with terraform


## Manually make a google oauth app to support social login (not supported in terraform unfortunately) 
I followed the instructions here:

Instead of updating your connection through the website, keep the client id and secret id for updating auth0 terraform.

## Manually make a github oath app to support social login (not supported in terraform unfortunately)
I followed the instructions here:
https://developer.auth0.com/resources/labs/authentication/authenticate-using-github#introduction
Instead of updating your connection through the website, keep the client id and secret id for updating auth0 terraform.

## Update auth0 terraform



