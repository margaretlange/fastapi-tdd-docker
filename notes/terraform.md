hashicorp vault
postman

What is a terraform module?
- a set of Terraform configuration files in a single diretory

Terraform commands will only directly use the configuration files in one directory, which is usually the current working directory. However, your configuration can use module blocks to call modules in other directories. When Terraform encounters a module block, it loads and processes that module's configuration files.

https://registry.terraform.io/modules/

You can reference module outputs in other parts of your configuration. Terraform will not display module outputs by default. You must create a corresponding output in your root module and set it to the module's output. This tutorial shows both cases.

tfstate
tfstate.backup

These files contain your Terraform state, and are how Terraform keeps track of the relationship between your configuration and the infrastructure provisioned by it.


.terraform

This directory contains the modules and plugins used to provision your infrastructure. These files are specific to a specific instance of Terraform when provisioning infrastructure, (sort of like .venv?)

.tfvars


I guess terraform init installs libraries so to speak
learn-terraform-modules-create

waaaa?
Notice that there is no provider block in this configuration. When Terraform processes a module block, it will inherit the provider from the enclosing configuration. Because of this, we recommend that you do not include provider blocks in modules.

When using a module, variables are set by passing arguments to the module in your configuration. You will set some of these variables when calling this module from your root module's main.tf.

You should also consider which values to add as outputs, since outputs are the only supported way for users to get information about resources configured by the module.

okay I think I just got api throttling great
it's 2:35 will wait an hour
#
https://spacelift.io/blog/importing-exisiting-infrastructure-into-terraform

# import tenant
terraform import auth0_tenant.tenant "82f4f21b-017a-319d-92e7-2291c1ca36c4"

# import management api
terraform import auth0_resource_server.auth0_management_api "67b8eaf065c050e148660318"
 resource auth0_resource_server auth0_management_api {
    identifer="unknown"
} 


Create application for management api
https://registry.terraform.io/providers/auth0/auth0/latest/docs/guides/quickstart
copy config locally
login
generate https://registry.terraform.io/providers/auth0/auth0/latest/docs/guides/generate_terraform_config

terraform {

  backend "s3" {
    bucket         = "mml-tf-state-authentication"
    key            = "global/s3/terraform.tfstate"
    region         = "us-west-2"
    use_lockfile = true
    encrypt        = true
  }

}

mv generate and import

https://stackoverflow.com/questions/55265203/terraform-delete-all-resources-except-one

I don't want these:
auth0_tenant.tenant
auth0_resource_server.auth0_management_api
auth0_client_grant.xbahqhxexauobrrnchqwfvuiebkvdrhb_https_dev_lhn1ufqgkgz8lk5w_us_auth0_com_api_v2
auth0_client_credentials.terraform_provider_auth0
auth0_client.terraform_provider_auth0
auth0_resource_server_scopes.auth0_management_api

pull out everything else generated
remove these above from state
destroy everything
reinit terraform
create everything minus management api stuff
