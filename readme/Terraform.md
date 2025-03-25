# How to provision infrastructure for the REST api and react frontend stub
- Note: Hopefully this isn't overkill. The more automated the better for a startup, I think. At least that was my experience at my last job.


### Repositories
- Terraform
  - aws backends for storing state
  - aws main for infrastructure
  - auth0 for infrastructure
- Fork of ollama deep researcher code
- My main app code

### Central secrets vault/Config store
- This time around both will be your local .bashrc or .bash_profile file.
- see secrets_and_config.txt in this folder for all the variables that will need to be set


### Accounts needed
- Amazon web services account (for basic infrastructure including server and database)
- google developer account (for setting up social authentication via google)
- github account (for accessing the repositories *and* for setting up social authentication for the app via github)
- auth0 account (for setting up app authentication system)
- register a domain or find one you don't mind using. I registered mmldemo.com on aws route53 and this config files worked for that setup. It may work for another setup, I'm not sure. (For route 53 signup the one gotcha was a confirmation email that kept going to my spam folder.) 
  

### Clients and Installations
- install terraform. I tested my infrastructure code using version 1.11.2, the latest version as of March 21, 2025.
  - https://developer.hashicorp.com/terraform/install
- install and configure the aws client using your aws identity

## Set up terraform backends using Terraform 
Set the following variables in your bash file	
   - export TF_VAR_aws_state_bucket_name
   - export TF_VAR_auth_state_bucket_name
   - export TF_VAR_region
- terraform init
- terraform validate
- terraform plan
- terraform apply

## Install aws infrastructure with terraform
- create a new ssh key for logging into the server or find an existing one you are comfortable with using that you haven't
already added to s3
- add the following variables to .bashrc or .bash_profile
   - TF_VAR_domain_name
   - TF_VAR_local_ssh_key_name
- modify the main.tf file's backend block by hand to include the correct bucket name and region, as this portion can't use
variables.
- terraform init
- terraform validate
- was able to get info about existing domain with `terraform plan -generate-config-out=generated.tf`
- terraform apply

## Manually make a google oauth app to support social login (not supported in terraform unfortunately) 
I followed the instructions here:

Instead of updating your connection through the website, keep the client id and secret id for updating auth0 terraform.
To do so add the following variables to your bash file:
- export TF_VAR_google_oauth_client_id
- export TF_VAR_google_oauth_client_secret

## Manually make a github oath app to support social login (not supported in terraform unfortunately)
I followed the instructions here:
https://developer.auth0.com/resources/labs/authentication/authenticate-using-github#introduction
Instead of updating your connection through the website, keep the client id and secret id for updating auth0 terraform.
To do so add the following variables to your bash file:

- export TF_VAR_github_oauth_client_id
- export TF_VAR_github_oauth_client_secret

## Install auth0 dependencies with terraform
Create an application to get the management api keys.  
https://registry.terraform.io/providers/auth0/auth0/latest/docs/guides/quickstart

Set up your tenant domain and management api keys in your bash environment
AUTH0_DOMAIN (your tenant domain)
AUTH0_CLIENT_ID (client id for your "explorer application")
AUTH0_CLIENT_SECRET (client secret id for your "explorer application"

Edit the s3 backend specification by hand to show the correct bucket.
Then you should be able to proceed
`terraform init`
- terraform validate
`terraform plan`
`terraform apply`

If you want to destroy all your auth0 infrastructure, you will need to destroy through terraform first and then manually destroy the management resources.
