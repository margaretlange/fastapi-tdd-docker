# How to provision infrastructure for the REST api and react frontend stub


## Clients and Installations
- [Install terraform](https://developer.hashicorp.com/terraform/install). I tested my infrastructure code using version 1.11.2, the latest version as of March 21, 2025.
- Install and configure the [aws client](https://aws.amazon.com/cli/) using your aws identity.
- Install and configure the [github client](https://cli.github.com/).

### Set up terraform backends in s3 using Terraform 
Folder is create-terraform-backend
Set the following variables in your bash file	
   - export TF_VAR_aws_state_bucket_name
   - export TF_VAR_auth_state_bucket_name
   - export TF_VAR_github_state_bucket_name
   - export TF_VAR_region
- terraform init
- terraform validate
- terraform plan
- terraform apply

### Install aws infrastructure with terraform
- Folder is learn-terraform-aws-instance
- Create a new ssh key for logging into the server or find an existing one you are comfortable with using that you haven't already added to aws.
- Add the following variables to .bashrc or .bash_profile
   - TF_VAR_domain_name
   - TF_VAR_local_ssh_key_name
- modify the main.tf file's backend block by hand to include the correct bucket name and region, as this portion can't use
variables.
- terraform init
- terraform validate
- was able to get info about existing domain with `terraform plan -generate-config-out=generated.tf` though the name servers will not be the correct ones
- terraform apply

- Manually Update at Registrar: You'll need to manually update the name servers at your domain registrar (e.g., GoDaddy, Namecheap) to match the ones assigned by AWS. 
  - Go to hosted zones, expand Hosted Zone details and copy the name servers
  - Go to domain name and edit name servers

### Manually make a google oauth app to support social login (not supported in terraform unfortunately) 
I followed [these instructions](https://developer.auth0.com/resources/labs/authentication/google-social-connection-to-login#introduction).

Instead of updating your connection through the website, keep the client id and secret id for updating auth0 terraform.
To do so add the following variables to your bash file:
- export TF_VAR_google_oauth_client_id
- export TF_VAR_google_oauth_client_secret

## Manually make a github oath app to support social login (not supported in terraform unfortunately)
I followed [these instructions](https://developer.auth0.com/resources/labs/authentication/authenticate-using-github#introduction).
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

## Install github actions variables with terraform
-gh auth login and then use that shell
- set TF_VAR_JWT_TEST_ENCODE_KEY to random 50 character string
     export TF_VAR_testing_api_ssh_private
 export TF_VAR_testing_api_ssh_public
export TF_VAR_main_repository
export TF_VAR_researcher_repository
initialize infrastructure via terraform

