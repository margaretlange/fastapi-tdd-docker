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

